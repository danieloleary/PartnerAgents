import { useState, useEffect, useRef } from 'react';

// We'll dynamically load pptxgenjs
let PptxGenJS = null;

export default function PptxViewer({ 
  src, 
  title = 'Presentation',
  onClose 
}) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [totalSlides, setTotalSlides] = useState(0);
  const [pres, setPres] = useState(null);
  const containerRef = useRef(null);

  useEffect(() => {
    async function loadPresentation() {
      try {
        setLoading(true);
        
        // Dynamically import pptxgenjs
        const module = await import('pptxgenjs');
        PptxGenJS = module.default;
        
        // Create presentation
        const presentation = new PptxGenJS();
        
        // Fetch the PPTX file
        const response = await fetch(src);
        const arrayBuffer = await response.arrayBuffer();
        
        // Load the presentation
        await presentation.load(arrayBuffer);
        setPres(presentation);
        setTotalSlides(presentation.slides.length);
        setLoading(false);
        
        // Render first slide
        renderSlide(presentation, 0);
      } catch (err) {
        console.error('Error loading presentation:', err);
        setError(err.message);
        setLoading(false);
      }
    }
    
    if (src) {
      loadPresentation();
    }
  }, [src]);

  function renderSlide(presentation, slideIndex) {
    if (!presentation || !containerRef.current) return;
    
    const slide = presentation.slides[slideIndex];
    containerRef.current.innerHTML = '';
    
    // Create slide container
    const slideDiv = document.createElement('div');
    slideDiv.style.cssText = `
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      flex-direction: column;
      padding: 48px;
      box-sizing: border-box;
      overflow: hidden;
      position: relative;
    `;
    
    // Brand bar at top
    const brandBar = document.createElement('div');
    brandBar.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: linear-gradient(90deg, #6366F1, #8B5CF6);
    `;
    slideDiv.appendChild(brandBar);
    
    // Content container
    const content = document.createElement('div');
    content.style.cssText = `
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      max-width: 900px;
      margin: 0 auto;
      width: 100%;
    `;
    
    // Try to extract and render text from the slide
    // This is a simplified renderer - full PPTX rendering is complex
    const textLines = [];
    
    // Check for text in shapes
    if (slide.shapes) {
      slide.shapes.forEach(shape => {
        if (shape.type === 'text' && shape.text) {
          textLines.push(shape.text);
        }
      });
    }
    
    if (textLines.length > 0) {
      // Render as text content
      const titleEl = document.createElement('h1');
      titleEl.textContent = textLines[0] || title;
      titleEl.style.cssText = `
        color: white;
        font-size: 36px;
        font-weight: 700;
        margin: 0 0 24px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      `;
      content.appendChild(titleEl);
      
      textLines.slice(1).forEach(line => {
        const p = document.createElement('p');
        p.textContent = line;
        p.style.cssText = `
          color: rgba(255,255,255,0.9);
          font-size: 18px;
          margin: 8px 0;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;
        content.appendChild(p);
      });
    } else {
      // Fallback - just show slide number
      const fallback = document.createElement('div');
      fallback.innerHTML = `
        <h1 style="color: white; font-size: 48px; font-weight: 700; margin: 0;">
          ${slideIndex + 1}
        </h1>
        <p style="color: rgba(255,255,255,0.7); font-size: 18px; margin-top: 16px;">
          Slide Content
        </p>
      `;
      content.appendChild(fallback);
    }
    
    slideDiv.appendChild(content);
    
    // Slide number
    const slideNum = document.createElement('div');
    slideNum.textContent = `${slideIndex + 1} / ${totalSlides}`;
    slideNum.style.cssText = `
      position: absolute;
      bottom: 20px;
      right: 30px;
      color: rgba(255,255,255,0.5);
      font-size: 14px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;
    slideDiv.appendChild(slideNum);
    
    containerRef.current.appendChild(slideDiv);
  }

  const nextSlide = () => {
    if (currentSlide < totalSlides - 1) {
      const next = currentSlide + 1;
      setCurrentSlide(next);
      renderSlide(pres, next);
    }
  };

  const prevSlide = () => {
    if (currentSlide > 0) {
      const prev = currentSlide - 1;
      setCurrentSlide(prev);
      renderSlide(pres, prev);
    }
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'Escape') {
        onClose?.();
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentSlide, totalSlides, pres]);

  if (loading) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.9)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        flexDirection: 'column',
        gap: 16,
      }}>
        <div style={{ 
          width: 48, 
          height: 48, 
          border: '3px solid rgba(255,255,255,0.2)',
          borderTopColor: '#6366F1',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
        }} />
        <style>{`
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}</style>
        <div style={{ color: 'white', fontSize: 16 }}>Loading presentation...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.9)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        flexDirection: 'column',
        gap: 20,
      }}>
        <div style={{ color: '#ef4444', fontSize: 16 }}>Error: {error}</div>
        <button 
          onClick={onClose}
          style={{
            background: 'white',
            border: 'none',
            padding: '10px 20px',
            cursor: 'pointer',
            borderRadius: 6,
            fontSize: 14,
          }}
        >
          Close
        </button>
      </div>
    );
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: '#111827',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
    }}>
      {/* Header */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        padding: '16px 24px',
        background: 'rgba(0,0,0,0.3)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        zIndex: 10,
        backdropFilter: 'blur(10px)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{
            width: 32,
            height: 32,
            background: 'linear-gradient(135deg, #6366F1, #8B5CF6)',
            borderRadius: 8,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 700,
            fontSize: 14,
          }}>
            P
          </div>
          <span style={{ color: 'white', fontSize: 16, fontWeight: 500 }}>
            {title}
          </span>
        </div>
        <button
          onClick={onClose}
          style={{
            background: 'transparent',
            border: '1px solid rgba(255,255,255,0.2)',
            color: 'white',
            padding: '8px 16px',
            cursor: 'pointer',
            borderRadius: 6,
            fontSize: 14,
            transition: 'all 0.2s',
          }}
        >
          Close (Esc)
        </button>
      </div>

      {/* Slide container */}
      <div 
        ref={containerRef}
        style={{
          width: '80%',
          maxWidth: 1000,
          aspectRatio: '16/9',
          borderRadius: 12,
          overflow: 'hidden',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        }}
      />

      {/* Navigation */}
      <div style={{
        position: 'absolute',
        bottom: 40,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 24,
      }}>
        <button
          onClick={prevSlide}
          disabled={currentSlide === 0}
          style={{
            background: currentSlide === 0 ? 'rgba(255,255,255,0.05)' : 'white',
            border: 'none',
            padding: '12px 28px',
            cursor: currentSlide === 0 ? 'default' : 'pointer',
            borderRadius: 8,
            fontSize: 14,
            fontWeight: 500,
            color: currentSlide === 0 ? 'rgba(255,255,255,0.3)' : '#111827',
            transition: 'all 0.2s',
          }}
        >
          ← Previous
        </button>
        
        <div style={{ 
          display: 'flex', 
          gap: 6,
          alignItems: 'center',
        }}>
          {Array.from({ length: totalSlides }).map((_, i) => (
            <div
              key={i}
              onClick={() => {
                setCurrentSlide(i);
                renderSlide(pres, i);
              }}
              style={{
                width: i === currentSlide ? 24 : 8,
                height: 8,
                background: i === currentSlide ? '#6366F1' : 'rgba(255,255,255,0.2)',
                borderRadius: 4,
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
            />
          ))}
        </div>
        
        <button
          onClick={nextSlide}
          disabled={currentSlide === totalSlides - 1}
          style={{
            background: currentSlide === totalSlides - 1 ? 'rgba(255,255,255,0.05)' : 'white',
            border: 'none',
            padding: '12px 28px',
            cursor: currentSlide === totalSlides - 1 ? 'default' : 'pointer',
            borderRadius: 8,
            fontSize: 14,
            fontWeight: 500,
            color: currentSlide === totalSlides - 1 ? 'rgba(255,255,255,0.3)' : '#111827',
            transition: 'all 0.2s',
          }}
        >
          Next →
        </button>
      </div>

      {/* Keyboard hint */}
      <div style={{
        position: 'absolute',
        bottom: 12,
        color: 'rgba(255,255,255,0.3)',
        fontSize: 12,
      }}>
        Use ← → arrow keys or Space to navigate • Press Esc to close
      </div>
    </div>
  );
}
