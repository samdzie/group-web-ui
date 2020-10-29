<template>
    <div id="group-home">
        <div id="group-header">
            <img
                v-bind:src="icon"
                id="group-icon"
            >
            <div id="group-welcome">
                <h1>{{ name }}</h1>
                <p>{{ welcome }}</p>
            </div>
        </div>
        <div id="group-about">
            <h2>About</h2>
            <p>{{ about }}</p>
        </div>
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
            icon: ''
        };
    },
    beforeMount() {
        this.getHome();
    },
    methods: {
        async getHome() {
            const baseURL = 'http://localhost:5000'
            const resp = await fetch(
                baseURL + '/api/group/' + this.groupID + '/home');
            const json = await resp.json();
            this.name = json.name;
            this.welcome = json.welcome;
            this.about = json.about;
            this.icon = json.icon;
        }
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
