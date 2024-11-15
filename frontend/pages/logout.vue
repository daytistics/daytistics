<script lang="ts" setup>
onMounted(() => {
    useAuthStore().logout();
    useRouter().push(document.referrer || '/');
});
</script>
