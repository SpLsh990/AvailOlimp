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
            if (!dropdown.contains(e.target)) {
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
const subjectFilter = document.getElementById('subjectFilter');
const difficultyFilter = document.getElementById('difficultyFilter');
const searchInput = document.getElementById('searchTask');
    const tasksList = document.getElementById('tasksList');
    const taskRows = document.querySelectorAll('.task-row');

    function filterTasks() {
        const subject = subjectFilter.value;
        const difficulty = difficultyFilter.value;
        const searchTerm = searchInput.value.toLowerCase();

        taskRows.forEach(row => {
            const subjectTag = row.querySelector('.subject-tag');
            const difficultyTag = row.querySelector('.difficulty-tag');
            const title = row.querySelector('.col-title').textContent.toLowerCase();

            let show = true;

            if (subject !== 'all') {
                const subjectClass = subjectTag.classList.contains(subject === 'physics' ? 'physics' : 'math');
                if (!subjectClass) show = false;
            }

            if (difficulty !== 'all') {
                const difficultyClass = difficultyTag.classList.contains(difficulty);
                if (!difficultyClass) show = false;
            }

            if (searchTerm && !title.includes(searchTerm)) {
                show = false;
            }

            row.style.display = show ? 'flex' : 'none';
        });
    }

    subjectFilter.addEventListener('change', filterTasks);
    difficultyFilter.addEventListener('change', filterTasks);
    searchInput.addEventListener('input', filterTasks);