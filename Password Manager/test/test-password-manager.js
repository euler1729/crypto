"use strict";

let expect = require('expect.js');
const { Keychain } = require('../password-manager');
const { BucketedKeychain } = require('../BucketedKeychain');
const { MultiUserKeychain } = require('../MultiUserKeychain');

function expectReject(promise) {
    return promise.then(
        (result) => expect().fail(`Expected failure, but function returned ${result}`),
        (error) => { },
    );
}

describe('Password manager', async function () {
    this.timeout(5000);
    let password = "password123!";
    let userId1 = "alice";
    let userId2 = "bob";

    let kvs = {
        "service1": "value1",
        "service2": "value2",
        "service3": "value3"
    };

    describe('functionality', async function () {

        it('inits Keychain without an error', async function () {
            await Keychain.init(password);
        });

        it('inits BucketedKeychain without an error', async function () {
            // await BucketedKeychain.init(password);
            new BucketedKeychain(10)
        });

        it('inits MultiUserKeychain without an error', async function () {
            await MultiUserKeychain.init(password);
        });

        it('can set and retrieve a password in Keychain', async function () {
            let keychain = await Keychain.init(password);
            let url = 'www.stanford.edu';
            let pw = 'sunetpassword';
            await keychain.set(url, pw);
            expect(await keychain.get(url)).to.equal(pw);
        });

        it('can set and retrieve a password in BucketedKeychain', async function () {
            let bucket = await BucketedKeychain.init(password);
            let url = 'www.stanford.edu';
            let pw = 'sunetpassword';
            await bucket.set(url, pw);
            expect(await bucket.get(url)).to.equal(pw);
        });

        // it('can set and retrieve a password with MultiUserKeychain', async function () {
        //     let keychain = await MultiUserKeychain.init(password);
        //     let url = 'www.stanford.edu';
        //     let pw = 'sunetpassword';
        //     await keychain.setForUser(userId1, url, pw);
        //     expect(await keychain.getForUser(userId1, url)).to.equal(pw);
        // });

        // it('can set and retrieve a password for different users with MultiUserKeychain', async function () {
        //     let keychain = new MultiUserKeychain();
        //     let url = 'www.stanford.edu';
        //     let pw1 = 'sunetpassword1';
        //     let pw2 = 'sunetpassword2';
        //     await keychain.setForUser(userId1, url, pw1);
        //     await keychain.setForUser(userId2, url, pw2);
        //     expect(await keychain.getForUser(userId1, url)).to.equal(pw1);
        //     expect(await keychain.getForUser(userId2, url)).to.equal(pw2);
        // });

        it('returns null for non-existent passwords in Keychain', async function () {
            let keychain = await Keychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            expect(await keychain.get('www.stanford.edu')).to.be(null);
        });

        it('returns null for non-existent passwords in BucketedKeychain', async function () {
            let keychain = await BucketedKeychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            expect(await keychain.get('www.stanford.edu')).to.be(null);
        });

        // it('returns null for non-existent passwords with MultiUserKeychain', async function () {
        //     let keychain = new MultiUserKeychain();
        //     let url = 'www.stanford.edu';
        //     expect(await keychain.getForUser(userId1, url)).to.be(null);
        // });

        it('can remove a password in Keychain', async function () {
            let keychain = await Keychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            expect(await keychain.remove('service1')).to.be(true);
            expect(await keychain.get('service1')).to.be(null);
        });

        it('can remove a password in BucketedKeychain', async function () {
            let keychain = await BucketedKeychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            expect(await keychain.remove('service1')).to.be(true);
            expect(await keychain.get('service1')).to.be(null);
        });

        // it('can remove a password with MultiUserKeychain', async function () {
        //     let keychain = new MultiUserKeychain();
        //     let url = 'www.stanford.edu';
        //     let pw = 'sunetpassword';
        //     await keychain.setForUser(userId1, url, pw);
        //     expect(await keychain.removeForUser(userId1, url)).to.be(true);
        //     expect(await keychain.getForUser(userId1, url)).to.be(null);
        // });

        it('returns false if there is no password for the domain being removed in Keychain', async function () {
            let keychain = await Keychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            expect(await keychain.remove('www.stanford.edu')).to.be(false);
        });

        it('returns false if there is no password for the domain being removed in BucketedKeychain', async function () {
            let keychain = await BucketedKeychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            expect(await keychain.remove('www.stanford.edu')).to.be(false);
        });

        it('fails to restore the database if checksum is wrong in Keychain', async function () {
            let keychain = await Keychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            let data = await keychain.dump();
            let contents = data[0];
            let fakeChecksum = '3GB6WSm+j+jl8pm4Vo9b9CkO2tZJzChu34VeitrwxXM=';
            await expectReject(Keychain.load(password, contents, fakeChecksum));
        });

        it('fails to restore the database if checksum is wrong in BucketedKeychain', async function () {
            let keychain = await BucketedKeychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            let data = await keychain.dump();
            let contents = data[0];
            let fakeChecksum = '3GB6WSm+j+jl8pm4Vo9b9CkO2tZJzChu34VeitrwxXM=';
            await expectReject(BucketedKeychain.load(password, contents, fakeChecksum));
        });

        it('returns false if trying to load with an incorrect password in Keychain', async function () {
            let keychain = await Keychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            let data = await keychain.dump();
            let contents = data[0];
            let checksum = data[1];
            await expectReject(Keychain.load("fakepassword", contents, checksum));
        });

        it('returns false if trying to load with an incorrect password in BucketedKeychain', async function () {
            let keychain = await BucketedKeychain.init(password);
            for (let k in kvs) {
                await keychain.set(k, kvs[k]);
            }
            let data = await keychain.dump();
            let contents = data[0];
            let checksum = data[1];
            await expectReject(BucketedKeychain.load("fakepassword", contents, checksum));
        });

    });

    describe('security', async function () {

        // Very basic test to make sure you're not doing the most naive thing
        it("doesn't store domain names and passwords in the clear in Keychain", async function () {
            let keychain = await Keychain.init(password);
            let url = 'www.stanford.edu';
            let pw = 'sunetpassword';
            await keychain.set(url, pw);
            let data = await keychain.dump();
            let contents = data[0];
            expect(contents).not.to.contain(password);
            expect(contents).not.to.contain(url);
            expect(contents).not.to.contain(pw);
        });

        // Very basic test to make sure you're not doing the most naive thing
        it("doesn't store domain names and passwords in the clear in BucketedKeychain", async function () {
            let keychain = await BucketedKeychain.init(password);
            let url = 'www.stanford.edu';
            let pw = 'sunetpassword';
            await keychain.set(url, pw);
            let data = await keychain.dump();
            let contents = data[0];
            expect(contents).not.to.contain(password);
            expect(contents).not.to.contain(url);
            expect(contents).not.to.contain(pw);
        });

        // This test won't be graded directly -- it just exists to make sure your
        // dump include a kvs object with all your urls and passwords, because
        // we will be using that in other tests.
        it('includes a kvs object in the serialized dump in Keychain', async function () {
            let keychain = await Keychain.init(password);
            for (let i = 0; i < 10; i++) {
                await keychain.set(String(i), String(i));
            }
            let data = await keychain.dump();
            let contents = data[0];
            let contentsObj = JSON.parse(contents);
            expect(contentsObj).to.have.key('kvs');
            expect(contentsObj.kvs).to.be.an('object');
            expect(Object.getOwnPropertyNames(contentsObj.kvs)).to.have.length(10);
        });

        // This test won't be graded directly -- it just exists to make sure your
        // dump include a kvs object with all your urls and passwords, because
        // we will be using that in other tests.
        it('includes a kvs object in the serialized dump in BucketedKeychain', async function () {
            let keychain = await BucketedKeychain.init(password);
            for (let i = 0; i < 10; i++) {
                await keychain.set(String(i), String(i));
            }
            let data = await keychain.dump();
            let contents = data[0];
            let contentsObj = JSON.parse(contents);
            expect(contentsObj).to.have.key('kvs');
            expect(contentsObj.kvs).to.be.an('object');
            expect(Object.getOwnPropertyNames(contentsObj.kvs)).to.have.length(10);
        });

    });
});
// module.exports = { MultiUserKeychain };
