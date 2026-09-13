import { useEffect, useRef } from "react";

function CursorGlow() {
  const dotRef = useRef(null);
  const glowRef = useRef(null);

  useEffect(() => {
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;

    let glowX = mouseX;
    let glowY = mouseY;

    let animationFrame;

    const textElements = [];

    const collectTextNodes = () => {
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        {
          acceptNode(node) {
            const parent = node.parentElement;

            if (!parent) {
              return NodeFilter.FILTER_REJECT;
            }

            const tag = parent.tagName.toLowerCase();

            if (
              tag === "script" ||
              tag === "style" ||
              tag === "input" ||
              tag === "textarea" ||
              tag === "button"
            ) {
              return NodeFilter.FILTER_REJECT;
            }

            if (!node.textContent.trim()) {
              return NodeFilter.FILTER_REJECT;
            }

            return NodeFilter.FILTER_ACCEPT;
          },
        }
      );

      let node;

      while ((node = walker.nextNode())) {
        const range = document.createRange();
        range.selectNodeContents(node);

        const rects = Array.from(range.getClientRects());

        rects.forEach((rect) => {
          textElements.push({
            node,
            rect,
          });
        });
      }
    };

    const updateTextHighlight = () => {
      let closest = null;
      let closestDistance = Infinity;

      textElements.forEach((item) => {
        const rect = item.node.parentElement?.getBoundingClientRect();

        if (!rect) {
          return;
        }

        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const distance = Math.sqrt(
          Math.pow(mouseX - centerX, 2) +
            Math.pow(mouseY - centerY, 2)
        );

        if (distance < closestDistance) {
          closestDistance = distance;
          closest = item.node.parentElement;
        }
      });

      document
        .querySelectorAll(".cursor-text-highlight")
        .forEach((element) => {
          element.classList.remove("cursor-text-highlight");
        });

      if (closest && closestDistance < 85) {
        closest.classList.add("cursor-text-highlight");
      }
    };

    const moveCursor = (event) => {
      mouseX = event.clientX;
      mouseY = event.clientY;

      if (dotRef.current) {
        dotRef.current.style.left = `${mouseX}px`;
        dotRef.current.style.top = `${mouseY}px`;
      }

      updateTextHighlight();
    };

    const animate = () => {
      glowX += (mouseX - glowX) * 0.12;
      glowY += (mouseY - glowY) * 0.12;

      if (glowRef.current) {
        glowRef.current.style.left = `${glowX}px`;
        glowRef.current.style.top = `${glowY}px`;
      }

      animationFrame = requestAnimationFrame(animate);
    };

    collectTextNodes();

    window.addEventListener("mousemove", moveCursor);
    window.addEventListener("resize", collectTextNodes);

    animationFrame = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener("mousemove", moveCursor);
      window.removeEventListener("resize", collectTextNodes);

      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }

      document
        .querySelectorAll(".cursor-text-highlight")
        .forEach((element) => {
          element.classList.remove("cursor-text-highlight");
        });
    };
  }, []);

  return (
    <>
      <div ref={glowRef} className="cursor-glow"></div>
      <div ref={dotRef} className="cursor-dot"></div>
    </>
  );
}

export default CursorGlow;