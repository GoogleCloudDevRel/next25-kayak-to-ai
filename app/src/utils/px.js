export function pxToVw(value, base = 1920) {
  return (value / base) * 100 + 'vw'
}

export function pxToVh(value, base = 1080) {
  return (value / base) * 100 + 'vh'
}

export function pxToVw4k(value, base = 4752) {
  return (value / base) * window.innerWidth
}

export function pxToVh4k(value, base = 2917) {
  return (value / base) * window.innerHeight
}
