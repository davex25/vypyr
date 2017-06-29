AC_PREREQ([2.69])
AC_INIT([Vypyr], [0.1])

AM_INIT_AUTOMAKE
AM_PATH_PYTHON([2.7])

PKG_CHECK_MODULES(gtk, [gtk+-3.0])
PKG_CHECK_MODULES(gmodule, [gmodule-export-2.0])
PKG_CHECK_MODULES([alsa], [alsa > 1.1])

AC_CONFIG_FILES([Makefile src/Makefile src/vypyr/Makefile])

AC_OUTPUT
