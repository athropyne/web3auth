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

    const add_address = async () => {
        
    }
</script>

<main>
    <div class="col address__list__wrapper">
        <ul class="address__list">
            {#each addresses as address (address)}
                <li class="address__text">{address}</li>
            {/each}
        </ul>
    </div>
    <div class="col add__address__form">
        <div class="form">
            <input
                    bind:value={new_address_value}
                    placeholder="добавмть адрес"
            >
            <button>отправить</button>
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

    .address__text {
        list-style-type: none;
    }
</style>