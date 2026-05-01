if (window.innerWidth <= 768) {
    const dropdown = document.querySelector('.dropdown');
    const dropdownBtn = document.querySelector('.dropdown-btn');

    if (dropdownBtn) {
        dropdownBtn.addEventListener('click', (e) => {
            e.preventDefault();
            dropdown.classList.toggle('active');
        });
    }

    document.addEventListener('click', (e) => {
        if (dropdown && !dropdown.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });
}


const profileAvatar = document.getElementById('profileAvatar');
const profileDropdownMenu = document.getElementById('profileDropdownMenu');

if (profileAvatar && profileDropdownMenu) {
    profileAvatar.addEventListener('click', (e) => {
        e.stopPropagation();
        profileDropdownMenu.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
        if (!profileAvatar.contains(e.target) && !profileDropdownMenu.contains(e.target)) {
            profileDropdownMenu.classList.remove('active');
        }
    });
}


function addHoverEffect() {
    const style = document.createElement('style');
    style.textContent = `
        .task-row {
            transition: background-color 0.3s ease;
            cursor: pointer;
        }
        .task-row:hover {
            background-color: rgba(59, 130, 246, 0.1) !important;
        }
    `;
    document.head.appendChild(style);
}


function makeTaskRowsClickable() {
    const taskRows = document.querySelectorAll('.task-row');
    
    taskRows.forEach(row => {
        if (row.hasAttribute('data-clickable')) return;
        
        const taskLink = row.querySelector('.task-link');
        if (taskLink) {
            const url = taskLink.getAttribute('href');
            
            row.addEventListener('click', function(e) {
                if (e.target.tagName !== 'A' && !e.target.closest('a')) {
                    window.location.href = url;
                }
            });
            
            row.setAttribute('data-clickable', 'true');
        }
    });
}


addHoverEffect();

document.addEventListener('DOMContentLoaded', function() {
    makeTaskRowsClickable();
});


const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            makeTaskRowsClickable();
        }
    });
});

const tasksTable = document.querySelector('.table-body');
if (tasksTable) {
    observer.observe(tasksTable, { childList: true, subtree: true });
}