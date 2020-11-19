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
                    v-bind:start="event.start"
                    v-bind:end="event.end"
                />
            </tbody>
        </table>
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
            this.events = json.events.slice();
        }
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
