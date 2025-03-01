import InputMicrophone from '@/components/InputMicrophone.vue'

const Template = (args) => ({
  components: { InputMicrophone },
  setup() {
    return { args }
  },
  template: /* html */ `
    <InputMicrophone v-bind="args" />
  `,
})

export const Primary = Template.bind({})
Primary.args = {
  cta: 'Start Recording',
  ctaStopped: 'Stop Recording',
  language: 'en-US',
}

export const Secondary = Template.bind({})
Secondary.args = {
  cta: 'Start Recording',
  ctaStopped: 'Stop Recording',
  language: 'en-US',
}

export default {
  title: 'Components/InputMicrophone',
  component: InputMicrophone,
  parameters: {
    layout: 'centered',
  },
}
