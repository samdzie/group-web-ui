<template>
    <tr v-if="editing">
        <td><input v-model="title_"></td>
        <td><input v-model="description_"></td>
        <td><input v-model="start_"></td>
        <td><input v-model="end_"></td>
        <td><button v-on:click="saveEvent">Save</button></td>
        <td><button v-on:click="deleteEvent">Delete</button></td>
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
        end: String,
        groupID: String,
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
            let data = {
                'title' : this.title_,
                'description' : this.description_,
                'start' : this.start_,
                'end' : this.end_,
            };
            let resp = await fetch('/api/group/' + this.groupID + '/events/' + this.id, {
                method : 'PUT',
                headers : {
                    'Content-Type' : 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (resp.ok) {
                this.editing = false;
            } else {
                alert('Error ' + resp.status + ' while saving event.');
            }
        },
        async deleteEvent() {
            let confirmation = confirm("Are you sure you want to delete this event?");
            if (confirmation) {
                let resp = await fetch('/api/group/' + this.groupID + '/events/' + this.id, {
                    method : 'DELETE',
                });
                if (resp.ok) {
                    this.$emit('delete-event');
                } else {
                    alert('Error ' + resp.status + ' while deleting event.');
                }
            }
        }
    }
}
</script>

<style scoped>
td {
    padding: 5px;
}
</style>
