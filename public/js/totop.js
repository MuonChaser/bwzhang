$(window).scroll(function() {
    $(window).scrollTop() > 500 ? $("#rocket").addClass("show") : $("#rocket").removeClass("show");
});
$("#rocket").click(function() {
    $("#rocket").addClass("launch");
    $("html, body").animate({
        scrollTop: 0
    }, 500, function() {
        $("#rocket").removeClass("show launch");
    });
    return false;
});

/* Sidebar toggle merged here so it loads with existing JS */
(function () {
    function setCollapsed(collapsed, btn) {
        if (collapsed) {
            document.body.classList.add('sidebar-collapsed');
            if (btn) btn.setAttribute('aria-expanded', 'false');
            if (btn) btn.textContent = '显示侧边栏';
        } else {
            document.body.classList.remove('sidebar-collapsed');
            if (btn) btn.setAttribute('aria-expanded', 'true');
            if (btn) btn.textContent = '隐藏侧边栏';
        }
    }

    function initSidebarToggle() {
        var btn = document.getElementById('sidebar-toggle');
        var sidebar = document.getElementById('secondary');
        if (!btn || !sidebar) return;

        // Click toggles (manual)
        btn.addEventListener('click', function () {
            var collapsed = document.body.classList.contains('sidebar-collapsed');
            setCollapsed(!collapsed, btn);
        });

        // check body data attribute to see if automatic collapse is enabled
        var autoEnabled = document.body && document.body.dataset && document.body.dataset.autoSidebarCollapse === 'true';
        if (autoEnabled) {
            var VISIBLE_THRESHOLD = 0.15; // 15%
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    var visible = entry.intersectionRatio > VISIBLE_THRESHOLD;
                    if (!visible) {
                        setCollapsed(true, btn);
                    } else {
                        setCollapsed(false, btn);
                    }
                });
            }, { root: null, threshold: [0, VISIBLE_THRESHOLD, 0.5] });

            observer.observe(sidebar);

            // Scroll direction: when user scrolls up significantly, show the sidebar
            var lastY = (window.pageYOffset || document.documentElement.scrollTop) || 0;
            window.addEventListener('scroll', function () {
                var y = window.pageYOffset || document.documentElement.scrollTop || 0;
                var delta = y - lastY;
                if (delta < -10) {
                    setCollapsed(false, btn);
                }
                lastY = y;
            }, { passive: true });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSidebarToggle);
    } else {
        initSidebarToggle();
    }
})();
