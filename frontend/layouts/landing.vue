<template>
<!--    <LandingNavBar class="z-50" />-->
  <LandingNavbar2 />
    <div class="min-h-screen flex flex-col font-inter z-10 relative">
        <slot></slot>
    </div>
    <hr />
    <LandingFooter />
</template>

<script setup lang="ts"></script>
