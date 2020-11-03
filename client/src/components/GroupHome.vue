<template>
    <div id="group-home">
        <div id="group-header">
            <img
                v-bind:src="icon"
                id="group-icon"
            >
            <div id="group-welcome">
                <form v-if="editing" v-on:submit="submitEdit">
                    <section>
                        <input v-model="name">
                    </section>
                    <section>
                        <textarea v-model="welcome"></textarea>
                    </section>
                </form>
                <div v-else>
                    <h1>{{ name }}</h1>
                    <p>{{ welcome }}</p>
                </div>
            </div>
        </div>
        <div id="group-about">
            <h2>About</h2>
            <form v-if="editing">
                <textarea v-model="about"></textarea>
            </form>
            <div v-else>
                <p>{{ about }}</p>
            </div>
        </div>
        <button v-if="editing" v-on:click="submitEdit">Save</button>
        <button v-else v-on:click="editing = true">Edit</button>
    </div>
</template>

<script>
export default {
    name: 'GroupHome',
    props: {
        groupID: String,
    },
    data: function() {
        return {
            name: '',
            welcome: '',
            about: '',
            icon: '',
            editing: false,
        };
    },
    beforeMount() {
        this.getHome();
    },
    methods: {
        async getHome() {
            const resp = await fetch('/api/group/' + this.groupID + '/home');
            const json = await resp.json();
            this.name = json.name;
            this.welcome = json.welcome;
            this.about = json.about;
            this.icon = json.icon;
        },
        async submitEdit() {
            let data = {
                'name' : this.name,
                'welcome' : this.welcome,
                'about' : this.about,
            };
            await fetch('/api/group/' + this.groupID + '/home', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            this.editing = false;
        },
    }
}
</script>

<style scoped>
#group-home {
    box-sizing: border-box;
    width: 100%;
    padding: 10px;
    background-color: lightgreen;
}
#group-header {
    display: flex;
    height: 200px;
}
#group-icon-container {
    height: 100%;
}
#group-icon {
    height: 100%;
}
#group-welcome {
    width: 100%;
    height: 100%;
    margin-left: 10px;
}
</style>
