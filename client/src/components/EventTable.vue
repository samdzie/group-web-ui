<template>
    <div>
        <table>
            <thead>
                <tr>
                    <th>Event</th>
                    <th>Description</th>
                    <th>Start</th>
                    <th>End</th>
                </tr>
            </thead>
            <tbody>
                <EventRow
                    v-for="event in events"
                    :key="event.id"
                    v-bind:id="event.id"
                    v-bind:title="event.title"
                    v-bind:description="event.description"
                    v-bind:start="event.start"
                    v-bind:end="event.end"
                    @delete-event="getEvents()"
                />
            </tbody>
        </table>
        <button @click="createEvent()">Create Event</button>
    </div>
</template>

<script>
import EventRow from './EventRow.vue'

export default {
    name: 'EventTable',
    components: {
        EventRow
    },
    props: {
        groupID: String,
    },
    data: function() {
        return {
            events: []
        };
    },
    beforeMount() {
        this.getEvents();
    },
    methods: {
        async getEvents() {
            const resp = await fetch('/api/group/' + this.groupID + '/events');
            const json = await resp.json();
            console.log(json);
            this.events = json.slice();
        },
        async createEvent() {
            let resp = await fetch('/api/group/' + this.groupID + '/events', {
                method : 'POST',
            });
            if (resp.ok) {
                this.getEvents();
            } else {
                alert('Error ' + resp.status + ' while creating event.');
            }
        },
    }
}
</script>

<style scoped>
div {
    box-sizing: border-box;
    padding: 10px;
    background-color: bisque;
}
table {
    width: 100%;
}
th {
    padding: 5px;
}
</style>
