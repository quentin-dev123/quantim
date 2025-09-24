export default function adjustColorBrightness(color, percent) {
    let num = parseInt(color.slice(1), 16);
    let amt = Math.round(2.55 * percent);
    let r = (num >> 16) + amt;
    let g = (num >> 8 & 0x00FF) + amt;
    let b = (num & 0x0000FF) + amt;

    r = Math.max(0, Math.min(255, r));
    g = Math.max(0, Math.min(255, g));
    b = Math.max(0, Math.min(255, b));

    return `#${(r << 16 | g << 8 | b).toString(16).padStart(6, '0')}`;
}