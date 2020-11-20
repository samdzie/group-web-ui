<template>
    <div id="group-home">
        <div id="group-header">
            <img
                v-bind:src="icon"
                id="group-icon"
            >
            <form v-if="editing" @submit="uploadIcon">
                <input
                    type="file"
                    accept="image/*"
                    @change="previewIcon($event)"
                    id="icon"
                >
            </form>
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
        <button v-if="editing" v-on:click="deleteGroup">Delete</button>
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
            if (resp.status == 404) {
                alert('Group not found.');
            } else if (!resp.ok) {
                alert('Error ' + resp.status + ' when fetching group.');
            } else {
                const json = await resp.json();
                this.name = json.name;
                this.welcome = json.welcome;
                this.about = json.about;
                this.icon = json.icon;
            }
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
        async deleteGroup() {
            let confirmation = confirm('Are you sure you want to delete this group?');
            if (confirmation) {
                let resp = await fetch('/api/group/' + this.groupID, {
                    method: 'DELETE',
                });
                if (resp.ok) {
                    location.reload();
                } else {
                    alert('Error ' + resp.status + ' while deleting group.');
                }
            }
        },
        async previewIcon(event) {
            let file = event.target.files[0];
            this.icon = window.URL.createObjectURL(file);
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
#group-icon {
    height: 200px;
    width: 200px;
    min-width: 200px;
}
#group-welcome {
    width: 100%;
    height: 100%;
    margin-left: 10px;
}
</style>
