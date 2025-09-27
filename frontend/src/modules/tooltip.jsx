// Tooltip.jsx
import React, { useState, useRef } from "react";

export default function Tooltip({ children, text, left = false }) {
    const [visible, setVisible] = useState(false);
    const [pos, setPos] = useState({ x: 0, y: 0 });
    const tooltipRef = useRef();
    const timeoutRef = useRef();

    const showTooltip = (e) => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        const x = left && tooltipRef.current
            ? e.clientX - tooltipRef.current.offsetWidth - 10
            : e.clientX + 10;
        const y = e.clientY + 10;
        timeoutRef.current = setTimeout(() => {
            setPos({ x, y });
            setVisible(true);
        }, 700);
    };

    const hideTooltip = () => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        setVisible(false);
    };

    return (
        <span
            className={left ? "tooltip_container_left" : "tooltip_container"}
            onMouseOver={showTooltip}
            onMouseMove={showTooltip}
            onMouseOut={hideTooltip}
        >
            {children}
            {visible && (
                <span
                    className="tooltip"
                    ref={tooltipRef}
                    style={{
                        opacity: 1,
                        position: "fixed",
                        left: pos.x,
                        top: pos.y,
                        zIndex: 1000,
                        pointerEvents: "none"
                    }}
                >
                    {text}
                </span>
            )}
        </span>
    );
}