<template>
    <div>
        <form v-on:submit.prevent="handleSubmit">
            <input id="groupIDInput" placeholder="Enter group ID">
            <button type="submit">View Group</button>
        </form>
        <div id="content" v-if="groupID">
            <GroupHome
                v-bind:groupID="groupID"
                v-bind:key="groupID"
            />
            <EventTable
                v-bind:groupID="groupID"
                v-bind:key="groupID"
            />
        </div>
    </div>
</template>

<script>
import EventTable from './components/EventTable.vue'
import GroupHome from './components/GroupHome.vue'

export default {
    name: 'App',
    components: {
        EventTable,
        GroupHome,
    },
    data: function() {
        return {
            groupID: undefined,
        };
    },
    methods: {
        handleSubmit() {
            this.groupID = document.getElementById("groupIDInput").value;
        },
    },
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    margin-left: auto;
    margin-right: auto;
    width: 800px;
}
form {
    margin: 10px;
}
form button {
    margin-left: 10px;
}
</style>
