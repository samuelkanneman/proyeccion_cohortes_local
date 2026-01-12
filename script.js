/**
 * SCRIPT.JS - UI Management
 * Maneja tabs, interacciones y UI elements
 */

// Tab switching
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(`tab-${targetTab}`).classList.add('active');
        });
    });
    
    console.log('UI initialized!');
});

// Smooth scroll to results when they appear
function scrollToResults() {
    const resultsPanel = document.getElementById('resultsPanel');
    if (resultsPanel && resultsPanel.style.display !== 'none') {
        resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Export helper functions
window.scrollToResults = scrollToResults;
