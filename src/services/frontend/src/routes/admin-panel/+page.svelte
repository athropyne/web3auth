<script>
    import {onMount} from "svelte";
    import {PUBLIC_SERVER_URI} from "$env/static/public";
    import {goto} from "$app/navigation";

    let addresses = $state()
    let new_address_value = $state()

    onMount(async () => {
        let response = await fetch(`${PUBLIC_SERVER_URI}/accounts`, {
            headers: {"Authorization": `Bearer ${localStorage.getItem("access_token")}`}
        })
        if (response.status === 401) {
            await goto("/")
        }
        addresses = await response.json()
        console.log(addresses)
    })

    const add_address = async (address) => {
        if (!address) return
        new_address_value = null
        let response = await fetch(`${PUBLIC_SERVER_URI}/accounts`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({address: address})
        })
        let data = await response.json()
        if (response.ok) {
            addresses.push(address)
        }
        else if (response.status === 401) {
            await goto("/")
        }
        else if (response.status === 400) {
            alert(data.detail)
        }
        else {
            console.log(data.detail)
        }
    }

    const delete_address = async (address) => {
        let response = await fetch(`${PUBLIC_SERVER_URI}/accounts/${address}`, {
                method: "DELETE",
                headers: {"Authorization": `Bearer ${localStorage.getItem("access_token")}`}
            }
        )
        if (response.ok) {
            let index = addresses.indexOf(address)
            addresses.splice(index, 1)
        }
        else if (response.status === 401) {
            await goto("/")
        }
        else if (response.status === 400 || response.status === 404 || response.status === 403) {
            let data = await response.json()
            alert(data.detail)
        }
        else {
            let data = await response.json()
            console.log(data.detail)
        }
    }



</script>

<main>
    <div class="col address__list__wrapper">
        <ul class="address__list">
            {#each addresses as address (address)}
                <li class="address__item">
                    <span class="address__text">{address}</span>
                    <button
                            class="address__delete__button"
                            onclick="{async () => await delete_address(address)}"

                    >X
                    </button>
                </li>
            {/each}
        </ul>
    </div>
    <div class="col add__address__form">
        <div class="form">
            <input
                    bind:value={new_address_value}
                    placeholder="добавить адрес"
            >
            <button
                onclick="{async () => await add_address(new_address_value)}"
            >отправить</button>
        </div>

    </div>
</main>

<style>
    main {
        display: flex;
        border: 1px black solid;
        height: 100vh;
    }

    .col {
        border: 1px solid black;
    }

    .address__list__wrapper {
        width: min-content;
    }

    .address__list {
        padding: 0 2em;
    }

    .add__address__form {
        width: 70%;
        position: relative;
    }

    .form {
        position: absolute;
        top: 50%;
        display: flex;
        width: 100%;
    }

    .form input {
        width: 100%;
    }

    .address__item {
        list-style-type: none;
        display: flex;
    }
    .address__delete__button {
        border: none;
    }
</style>