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