<script>
    import {onMount} from "svelte";
    import Web3 from "web3";
    import {PUBLIC_SERVER_URI} from "$env/static/public";
    import {goto} from "$app/navigation";

    let w3 = $state()
    // let message = 'sign this message please'
    let error_msg = $state(null)



    onMount(async () => {
        if (typeof window.ethereum != 'undefined') {
            w3 = new Web3(window.ethereum)
        } else {
            alert("дла работы необходимо расширение metamask")
            window.location.replace("https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn?hl=ru")
        }
    })
    const auth = async () => {
        await window.ethereum.request({
            method: 'eth_requestAccounts'
        });
        const accounts = await w3.eth.getAccounts()
        let address = accounts[0]
        let message = Math.random().toString(36).substring(2)
        let signature = await w3.eth.personal.sign(message, address, '')
        let auth_data = {
            address: address,
            message: message,
            signature: signature
        }
        let response = await fetch(`${PUBLIC_SERVER_URI}/security`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(auth_data)
        })
        let data = await response.json()
        if (response.status === 403) {
            alert(data.detail)
        }
        else {
            localStorage.setItem("access_token", data["access_token"])
            await goto("/admin-panel")
        }
    }
</script>
<main>

    <button onclick="{auth}">SIGN</button>
</main>