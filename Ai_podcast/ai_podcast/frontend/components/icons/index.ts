export const Icons = {
    play: '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>',
    pause: '<svg viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>',
    upload: '<svg viewBox="0 0 24 24"><path d="M9 16h6v-6h4l-7-7-7 7h4v6zm-4 2h14v2H5v-2z"/></svg>',
    // ... 添加其他需要的图标
};

export function createIcon(name: keyof typeof Icons): HTMLElement {
    const div = document.createElement('div');
    div.className = 'icon';
    div.innerHTML = Icons[name];
    return div;
} 