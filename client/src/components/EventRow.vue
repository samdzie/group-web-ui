<template>
    <tr v-if="editing">
        <td><input v-model="title_"></td>
        <td><input v-model="description_"></td>
        <td><input v-model="start_"></td>
        <td><input v-model="end_"></td>
        <td><button v-on:click="saveEvent">Save</button></td>
    </tr>
    <tr v-else>
        <td>{{ title_ }}</td>
        <td>{{ description_ }}</td>
        <td>{{ start_ }}</td>
        <td>{{ end_ }}</td>
        <td><button v-on:click="editing = true">Edit</button></td>
    </tr>
</template>

<script>
export default {
    name: 'EventRow',
    props: {
        id: String,
        title: String,
        description: String,
        start: String,
        end: String
    },
    data: function() {
        return {
            editing: false,
            title_: this.title,
            description_: this.description,
            start_: this.start,
            end_: this.end
        };
    },
    methods: {
        async saveEvent() {
            alert("saved event!");
            this.editing = false;
        },
    }
}
</script>

<style scoped>
td {
    padding: 5px;
}
</style>
