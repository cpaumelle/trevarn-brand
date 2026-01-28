<script setup lang="ts">
/**
 * Trevarn Icon Component
 * ======================
 * Renders icons from the Trevarn icon sprite.
 *
 * Usage:
 *   <Icon name="user" />
 *   <Icon name="health-heart" size="24" class="text-trevarn-glaz-400" />
 *   <Icon name="alert-triangle" title="Warning" />
 *
 * Rules:
 * - Icons inherit colour via currentColor (use Tailwind text-* classes)
 * - Never hard-code colours in icons
 * - Context sets colour, not the icon
 */
import type { TrevarnIconName } from "@/icons/trevarn-icons"

const props = withDefaults(
  defineProps<{
    /** Icon ID from trevarn-icons registry */
    name: TrevarnIconName
    /** Icon size in pixels (default: 20) */
    size?: number | string
    /** Accessible title (adds <title> element) */
    title?: string
  }>(),
  {
    size: 20,
  }
)
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.75"
    stroke-linecap="round"
    stroke-linejoin="round"
    :aria-hidden="!title"
    :aria-label="title"
    role="img"
  >
    <title v-if="title">{{ title }}</title>
    <use :href="`/icons/trevarn-icons.svg#icon-${name}`" />
  </svg>
</template>
