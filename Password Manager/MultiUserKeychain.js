const { Keychain } = require('./password-manager');
const { stringToBuffer, bufferToString, encodeBuffer, decodeBuffer, getRandomBytes } = require("./lib");
const { pbkdf2, randomInt } = require('crypto');
const { subtle, getRandomValues } = require('crypto').webcrypto;


class MultiUserKeychain extends Keychain {
    constructor() {
        super();
        this.userKeys = {}; // Store user-specific keys
    }

    // Generate a user-specific key
    generateUserKey(userId) {
        const userKey = getRandomBytes(32); // Generate a random key for each user
        this.userKeys[userId] = userKey;
        return userKey;
    }

    // Store a password for a site
    async setForUser(userId, site, rawPassword) {
        let domainKey = await subtle.sign(
            "HMAC", this.secrets.domainKey, stringToBuffer(site)
        );
        domainKey = encodeBuffer(domainKey);

        const userKey = this.userKeys[userId] || this.generateUserKey(userId); // Get or generate user key

        const securePassword =
            rawPassword + domainKey + encodeBuffer(getRandomBytes(randomInt(32, 64)));

        const iv = getRandomBytes(24);
        let encryptedPassword = await subtle.encrypt(
            {
                name: "AES-GCM",
                iv: iv,
            },
            await subtle.deriveKey(
                {
                    name: "PBKDF2",
                    salt: domainKey,
                    iterations: ITERATIONS,
                    hash: "SHA-256",
                },
                userKey,
                { name: "AES-GCM", length: 256 },
                false,
                ["encrypt", "decrypt"]
            ),
            stringToBuffer(securePassword)
        );
        encryptedPassword = encodeBuffer(iv) + encodeBuffer(encryptedPassword);

        const bucketIndex = hashString(site) % this.bucketCount;
        this.buckets[bucketIndex][domainKey] = encryptedPassword;
    }

    // Retrieve a password for a site for a specific user
    async getForUser(userId, site) {
        const domainKey = await subtle.sign(
            "HMAC", this.secrets.domainKey, stringToBuffer(site)
        );
        const userKey = this.userKeys[userId];
        if (!userKey) return null; // User doesn't have access to any passwords

        const bucketIndex = hashString(site) % this.bucketCount;
        const encryptedPassword = this.buckets[bucketIndex][encodeBuffer(domainKey)];
        if (!encryptedPassword) return null;

        const iv = encryptedPassword.slice(0, 32);
        const encrypted = encryptedPassword.slice(32);
        const decryptedPassword = await subtle.decrypt(
            {
                name: "AES-GCM",
                iv: decodeBuffer(iv),
            },
            await subtle.deriveKey(
                {
                    name: "PBKDF2",
                    salt: domainKey,
                    iterations: ITERATIONS,
                    hash: "SHA-256",
                },
                userKey,
                { name: "AES-GCM", length: 256 },
                false,
                ["encrypt", "decrypt"]
            ),
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

    // Remove a password for a site for a specific user
    async removeForUser(userId, site) {
        const domainKey = await subtle.sign(
            "HMAC", this.secrets.domainKey, stringToBuffer(site)
        );
        const bucketIndex = hashString(site) % this.bucketCount;
        if (this.buckets[bucketIndex][encodeBuffer(domainKey)]) {
            delete this.buckets[bucketIndex][encodeBuffer(domainKey)];
            return true;
        }
        return false;
    }
}
module.exports = { MultiUserKeychain };