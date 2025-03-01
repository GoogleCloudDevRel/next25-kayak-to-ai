import fs from 'fs'
import path from 'path'

function generateStoryTemplate(componentName) {
  return `import ${componentName} from '@/components/${componentName}.vue'

const Template = (args) => ({
  components: { ${componentName} },
  setup() {
    return { args }
  },
  template: '<${componentName} v-bind="args" />',
})

export const Primary = Template.bind({})
Primary.args = {
}

export const Secondary = Template.bind({})
Secondary.args = {
}

export default {
  title: 'Components/${componentName}',
  component: ${componentName},
  parameters: {
    layout: 'centered',
  },
}
`
}

function generateComponentTemplate(componentName) {
  return `<template>
  <div class="${componentName.toLowerCase()}">
    ${componentName} Component
  </div>
</template>

<script setup>
defineProps({
})
</script>

<style lang="scss">

.${componentName.toLowerCase()} {
}
</style>
`
}

function createStoryFile() {
  const componentName = process.argv[2]

  if (!componentName) {
    console.error('Please provide a component name')
    console.log('Usage: node generate-story.js ComponentName')
    process.exit(1)
  }

  const storiesDir = './src/stories'
  const componentsDir = './src/components'
  const storyPath = path.join(storiesDir, `${componentName}.stories.js`)
  const cssFilePath = path.join(storiesDir, `${componentName}.scss`)
  const componentPath = path.join(componentsDir, `${componentName}.vue`)

  const allDirs = [storiesDir, componentsDir]

  allDirs.forEach((dir) => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true })
    }
  })

  // Create css file if it doesn't exist
  if (!fs.existsSync(cssFilePath)) {
    fs.writeFileSync(cssFilePath, '')
  }

  // Generate and write the component file
  fs.writeFileSync(componentPath, generateComponentTemplate(componentName))
  console.log(`Created component file: ${componentPath}`)

  // Generate and write the story file
  fs.writeFileSync(storyPath, generateStoryTemplate(componentName))
  console.log(`Created story file: ${storyPath}`)
}

createStoryFile()
