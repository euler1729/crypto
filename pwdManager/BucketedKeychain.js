const { Keychain } = require('./password-manager');
const { stringToBuffer, bufferToString, encodeBuffer, decodeBuffer, getRandomBytes } = require("./lib");
const { pbkdf2, randomInt } = require('crypto');
const { subtle, getRandomValues } = require('crypto').webcrypto;

/********* Constants ********/
const ITERATIONS = 10000; // number of iterations for PBKDF2 algorithm


class BucketedKeychain extends Keychain {
    constructor(bucketCount=10) {
        super();
        this.bucketCount = bucketCount;
        this.buckets = Array.from({ length: bucketCount }, () => ({}));
        this.keychain = new Keychain();
    }

    async init(password){
        this.keychain = this.keychain.init(password);
    }

    async set(name, rawPassword) {
        let domainKey = await subtle.sign(
            "HMAC", this.keychain.secrets.domainKey, stringToBuffer(name)
        );
        domainKey = encodeBuffer(domainKey);

        const securePassword =
            rawPassword + domainKey + encodeBuffer(getRandomBytes(randomInt(32, 64)));

        const iv = getRandomBytes(24);
        let encryptedPassword = await subtle.encrypt(
            {
                name: "AES-GCM",
                iv: iv,
            },
            this.keychain.secrets.passwordKey,
            stringToBuffer(securePassword)
        );
        encryptedPassword = encodeBuffer(iv) + encodeBuffer(encryptedPassword);

        const bucketIndex = hashString(name) % this.bucketCount;
        this.buckets[bucketIndex][domainKey] = encryptedPassword;
    }

    async get(name) {
        const domainKey = await subtle.sign(
            "HMAC", this.keychain.secrets.domainKey, stringToBuffer(name)
        );
        const bucketIndex = hashString(name) % this.bucketCount;
        const encryptedPassword = this.buckets[bucketIndex][encodeBuffer(domainKey)];

        if (!encryptedPassword) return null;

        const iv = encryptedPassword.slice(0, 32);
        const encrypted = encryptedPassword.slice(32);
        const decryptedPassword = await subtle.decrypt(
            {
                name: "AES-GCM",
                iv: decodeBuffer(iv),
            },
            this.keychain.secrets.passwordKey,
            decodeBuffer(encrypted)
        );

        const password = bufferToString(decryptedPassword);
        const secureDomainIndex = password.indexOf(encodeBuffer(domainKey));
        if (secureDomainIndex === -1) {
            console.log("Possible Swap Attack");
            return null;
        }
        return password.slice(0, secureDomainIndex);
    }

    async count() {
        let count = 0;
        for (const bucket of this.buckets) {
            count += Object.keys(bucket).length;
        }
        return count;
    }
}

// Hash function for bucketing
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = (hash << 5) - hash + str.charCodeAt(i);
        hash |= 0; // Convert to 32-bit integer
    }
    return hash;
}

module.exports = { BucketedKeychain };