<template>
    <tr>
        <td>{{ title }}</td>
        <td>{{ start }}</td>
        <td>{{ end }}</td>
    </tr>
</template>

<script>
export default {
    name: 'EventRow',
    props: {
        title: String,
        start: String,
        end: String
    }
}
</script>

<style scoped>
td {
    padding: 5px;
}
</style>
