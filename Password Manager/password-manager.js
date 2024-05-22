"use strict";

/********* External Imports ********/

const { stringToBuffer, bufferToString, encodeBuffer, decodeBuffer, getRandomBytes } = require("./lib");
const { pbkdf2, randomInt } = require('crypto');
const { subtle, getRandomValues } = require('crypto').webcrypto;

/********* Constants ********/
const ITERATIONS = 10000; // number of iterations for PBKDF2 algorithm

class Keychain {
  /**
   * Initializes the keychain using the provided information. Note that external
   * users should likely never invoke the constructor directly and instead use
   * either Keychain.init or Keychain.load.
   * Arguments:
   *  You may design the constructor with any parameters you would like.
   * @return: void
   */
  constructor() {

    this.data = {
      kvs: null,
      keyHash: null,
      masterSalt: null,
      domainSalt: null,
      passwordSalt: null,
    };

    this.secrets = {
      masterKey: null,
      masterPassword: null,
      domainKey: null,
      passwordKey: null,
    };
  }

  /**
   * Creates an empty keychain with the given password.
   *
   * Arguments:
   * @param  password: string
   * @return: void
   */
  static async init(password, masterSalt = null, domainSalt = null, passwordSalt = null, passwordHash = null) {

    const keychain = new Keychain(); // create a new keychain object
    keychain.data.kvs = {}; // initialize the key-value store

    if (masterSalt === null) masterSalt = getRandomBytes(128);
    if (domainSalt === null) domainSalt = getRandomBytes(128);
    if (passwordSalt === null) passwordSalt = getRandomBytes(128);

    keychain.data.masterSalt = masterSalt; // store the master salt
    keychain.data.domainSalt = domainSalt; // store the domain salt
    keychain.data.passwordSalt = passwordSalt; // store the password salt

    // Convert the password to a buffer
    const passworBuffer = stringToBuffer(password);

    // Import the password as a key
    const masterKey = await subtle.importKey("raw", passworBuffer, { name: "PBKDF2" }, false, ["deriveKey"]);

    /*
    The master key is derived using the PBKDF2 algorithm with the following parameters:
    - salt: masterSalt
    - iterations: 10000
    - hash: SHA-256
    - key length: 256 bits
    - password: password
    - key usage: HMAC with SHA-256
    - extractable: true
    - key algorithm: HMAC with SHA-256
    - key usage: sign, verify
    */
    keychain.secrets.masterKey = await subtle.deriveKey(
      {
        name: "PBKDF2",
        salt: keychain.data.masterSalt,
        iterations: ITERATIONS,
        hash: "SHA-256",
      },
      masterKey,
      { name: "HMAC", hash: "SHA-256" },
      true,
      ["sign", "verify"]
    );

    // Derive the key hash from the master key
    keychain.data.keyHash = await subtle.digest("SHA-256", await subtle.exportKey("raw", keychain.secrets.masterKey));
    keychain.data.keyHash = encodeBuffer(keychain.data.keyHash);

    // Check if the password hash is provided and if it matches the key hash
    if (passwordHash !== null && keychain.data.keyHash !== passwordHash) {
      throw new Error("Invalid password hash");
    }

    // Derive the domain key from the master key
    const extractedRawMasterKeyForDomain = await subtle.sign(
      "HMAC", keychain.secrets.masterKey, keychain.data.domainSalt);
    // console.log(extractedRawMasterKeyForDomain)
    keychain.secrets.domainKey = await subtle.importKey(
      "raw", extractedRawMasterKeyForDomain, { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
    );

    // Derive the password key from the master key
    const extractedRawMasterKeyForPassword = await subtle.sign(
      "HMAC", keychain.secrets.masterKey, keychain.data.passwordSalt
    );
    // console.log(extractedRawMasterKeyForPassword)
    keychain.secrets.passwordKey = await subtle.importKey(
      "raw", extractedRawMasterKeyForPassword, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]
    );

    return keychain;
  }

  /**
   * Loads the keychain state from the provided representation (repr). The
   * repr variable will contain a JSON encoded serialization of the contents
   * of the KVS (as returned by the dump function). The trustedDataCheck
   * is an *optional* SHA-256 checksum that can be used to validate the
   * integrity of the contents of the KVS. If the checksum is provided and the
   * integrity check fails, an exception should be thrown. You can assume that
   * the representation passed to load is well-formed (i.e., it will be
   * a valid JSON object).Returns a Keychain object that contains the data
   * from repr.
   *
   * Arguments:
   * @param  password:           string
   * @param  data_json:               string
   * @param  trustedDataCheck: string
   * @return keychain: Keychain
   */
  static async load(password, data_json, trustedDataCheck) {

    if (trustedDataCheck) { // Check if the checksum is provided
      const checksum = await subtle.digest("SHA-256", stringToBuffer(data_json));
      const checksumString = encodeBuffer(checksum);
      if (checksumString !== trustedDataCheck) { // Check if the checksum matches
        throw new Error("Integrity check failed");
      }
    }

    // Parse the JSON representation
    const data = JSON.parse(data_json);

    // Extract the data from the JSON representation
    const masterSalt = Buffer.from(Object.values(data.masterSalt));
    const domainSalt = Buffer.from(Object.values(data.domainSalt));
    const passwordSalt = Buffer.from(Object.values(data.passwordSalt));
    const passwordHash = data.keyHash; // password hash
    const kvs = data.kvs; // key-value store

    // Check if the data is valid
    if (
      masterSalt === undefined ||
      domainSalt === undefined ||
      passwordSalt === undefined ||
      passwordHash == undefined ||
      kvs === undefined
    ) {
      throw new Error("Invalid data");
    }

    // Initialize the keychain
    const keychain = await Keychain.init(
      password, masterSalt, domainSalt, passwordSalt, passwordHash
    );
    // Set the key-value store
    keychain.data.kvs = kvs;
    return keychain;
  }

  /**
   * Returns a JSON serialization of the contents of the keychain that can be
   * loaded back using the load function. The return value should consist of
   * an array of two strings:
   *   arr[0] = JSON encoding of password manager
   *   arr[1] = SHA-256 checksum (as a string)
   * As discussed in the handout, the first element of the array should contain
   * all of the data in the password manager. The second element is a SHA-256
   * checksum computed over the password manager to preserve integrity.
   *
   * Return Type: array
   */
  async dump() {
    const repr = JSON.stringify(this.data);
    const checksum = await subtle.digest("SHA-256", stringToBuffer(repr));
    const checksumString = encodeBuffer(checksum);
    return [repr, checksumString];
  }

  /**
   * Fetches the data (as a string) corresponding to the given domain from the KVS.
   * If there is no entry in the KVS that matches the given domain, then return
   * null.
   *
   * Arguments:
   * @param  name: string
   * @return Type: Promise<string>
   */
  async get(name) {

    let domainKey = await subtle.sign(
      "HMAC", this.secrets.domainKey, stringToBuffer(name)
    );
    domainKey = encodeBuffer(domainKey);

    // if the domain is not in the KVS, return null
    if (this.data.kvs[domainKey] === undefined) return null;

    const encryptedPassword = this.data.kvs[domainKey]; // get the encrypted password
    const iv = encryptedPassword.slice(0, 32); // get the IV
    const encrypted = encryptedPassword.slice(32); // get the encrypted password

    // Decrypt the password
    const decryptedPassword = await subtle.decrypt(
      {
        name: "AES-GCM",
        iv: decodeBuffer(iv),
      },
      this.secrets.passwordKey,
      decodeBuffer(encrypted)
    );

    // Convert the decrypted password to a string
    const password = bufferToString(decryptedPassword);

    // Check if the domain key is present in the password
    const secureDomainIndex = password.indexOf(domainKey);
    if (secureDomainIndex === -1) {
      console.log("Possible Swap Attack");
      return null;
    }
    return password.slice(0, secureDomainIndex);
  }

  /**
   * Inserts the domain and associated data into the KVS. If the domain is
   * already in the password manager, this method should update its value. If
   * not, create a new entry in the password manager.
   *
   * Arguments:
   *   name: string
   *   value: string
   * Return Type: void
   */
  async set(name, rawPassword) {
    // create the domain key
    let domainKey = await subtle.sign(
      "HMAC", this.secrets.domainKey, stringToBuffer(name)
    );
    domainKey = encodeBuffer(domainKey);

    // generate a random password
    const securePassword =
      rawPassword + domainKey + encodeBuffer(getRandomBytes(randomInt(32, 64)));

    // encrypt the password
    const iv = getRandomBytes(24);
    let encryptedPassword = await subtle.encrypt(
      {
        name: "AES-GCM",
        iv: iv,
      },
      this.secrets.passwordKey,
      stringToBuffer(securePassword)
    );
    encryptedPassword = encodeBuffer(iv) + encodeBuffer(encryptedPassword);

    // store the encrypted password in the KVS
    this.data.kvs[domainKey] = encryptedPassword;
  }

  /**
   * Removes the record with name from the password manager. Returns true
   * if the record with the specified name is removed, false otherwise.
   *
   * Arguments:
   * @param  name: string
   * @return Type: Promise<boolean>
   */
  async remove(name) {
    // create the domain key
    let domainKey = await subtle.sign(
      "HMAC", this.secrets.domainKey, stringToBuffer(name)
    );
    domainKey = encodeBuffer(domainKey);

    // remove the domain key from the KVS
    if (this.data.kvs[domainKey] !== undefined) {
      delete this.data.kvs[domainKey];
      return true;
    }
    return false;
  }

  async createSHA256Hash(data) {
    const hash = subtle.digest('SHA-256', stringToBuffer(data));
    return encodeBuffer(hash);
  }
  async setForUser(userId, site, rawPassword){}
  async getForUser(userId, site){}
}


module.exports = { Keychain };
