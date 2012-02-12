Summary:        GNU Image Manipulation Program
Name:           gimp
Epoch:          2
Version:        2.8.0
Release:        2%{?dist}
License:        GPLv3+
Group:          Applications/Multimedia
URL:            http://www.gimp.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%__id_u -n)
Obsoletes:      gimp-perl < 2:2.0
Obsoletes:      gimp < 2:2.6.0-3
BuildRequires:  chrpath >= 0.13-5
BuildRequires:  aalib-devel
BuildRequires:  alsa-lib-devel >= 1.0.0
BuildRequires:  babl-devel >= 0.1.6
BuildRequires:  cairo-devel >= 1.10.2
BuildRequires:  curl-devel >= 7.15.1
BuildRequires:  dbus-glib-devel >= 0.70
BuildRequires:  fontconfig-devel >= 2.2.0
BuildRequires:  freetype-devel >= 2.1.7
BuildRequires:  gdk-pixbuf2-devel >= 2.24.0
BuildRequires:  gegl-devel >= 0.1.8
BuildRequires:  glib2-devel >= 2.30.2
BuildRequires:  gnome-keyring-devel >= 0.4.5
BuildRequires:  gtk2-devel >= 2.24.7
BuildRequires:  gtk-doc >= 1.0
BuildRequires:  jasper-devel
BuildRequires:  lcms-devel >= 1.16
BuildRequires:  libexif-devel >= 0.6.15
BuildRequires:  libgnomeui-devel >= 2.10.0
BuildRequires:  libgudev1-devel >= 167
BuildRequires:  libjpeg-devel
BuildRequires:  libmng-devel
BuildRequires:  libpng-devel >= 1.2.37
BuildRequires:  librsvg2-devel >= 2.34.2
BuildRequires:  libtiff-devel
BuildRequires:  libwmf-devel >= 0.2.8
BuildRequires:  pango-devel >= 1.29.4
BuildRequires:  poppler-glib-devel >= 0.12.4
BuildRequires:  poppler-devel >= 0.12.4
BuildRequires:  python-devel
BuildRequires:  pygtk2-devel >= 2.10.4
BuildRequires:  pygobject2-devel
BuildRequires:  webkitgtk-devel >= 1.6.1
BuildRequires:  libX11-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXpm-devel
BuildRequires:  sed
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  findutils

Requires:       glib2 >= 2.28.8
Requires:       gtk2 >= 2.24.7
Requires:       pango >= 1.29.4
Requires:       freetype >= 2.1.7
Requires:       fontconfig >= 2.2.0
Requires:       hicolor-icon-theme
Requires:       pygtk2 >= 2.10.4
Requires:       xdg-utils
Requires:       gimp-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Source0:        ftp://ftp.gimp.org/pub/gimp/v%{binver}/gimp-%{version}.tar.bz2

%description
GIMP (GNU Image Manipulation Program) is a powerful image composition and
editing program, which can be extremely useful for creating logos and other
graphics for webpages. GIMP has many of the tools and filters you would expect
to find in similar commercial offerings, and some interesting extras as well.
GIMP provides a large image manipulation toolbox, including channel operations
and layers, effects, sub-pixel imaging and anti-aliasing, and conversions, all
with multi-level undo.

%package libs
Summary:        GIMP libraries
Group:          System Environment/Libraries
License:        LGPLv3+

%description libs
The gimp-libs package contains shared libraries needed for the GNU Image
Manipulation Program (GIMP).

%package devel
Summary:        GIMP plugin and extension development kit
Group:          Development/Libraries
License:        LGPLv3+
Requires:       gimp-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       gimp-devel-tools = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       gtk2-devel
Requires:       glib2-devel
Requires:       pkgconfig

%description devel
The gimp-devel package contains the static libraries and header files
for writing GNU Image Manipulation Program (GIMP) plug-ins and
extensions.

%package devel-tools
Summary:        GIMP plugin and extension development tools
Group:          Development/Tools
License:        LGPLv3+
Requires:       gimp-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel-tools
The gimp-devel-tools package contains gimptool, a helper program to build GNU
Image Manipulation Program (GIMP) plug-ins and extensions.

%package help-browser
Summary:        GIMP help browser plug-in
Group:          Applications/Multimedia
License:        GPLv3+
Obsoletes:      gimp < 2:2.6.0-3
Requires:       gimp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description help-browser
The gimp-help-browser package contains a lightweight help browser plugin for
viewing GIMP online help.

%prep
%setup -q -n gimp-%{version}

%build
%configure \
    --enable-python \
    --disable-python \
    --enable-mp \
    --disable-static \
    --with-print \
    --with-lcms \
    --without-lcms \
    --enable-gimp-console \
    --with-aa \
    --with-gudev --without-hal \
    --with-linux-input \
    --with-poppler \
    --with-libtiff \
    --with-libjpeg \
    --with-libpng \
    --with-libmng \
    --with-libjasper \
    --with-libexif \
    --with-librsvg \
    --with-libxpm \
    --with-gvfs \
    --with-alsa \
    --with-webkit \
    --with-dbus \
    --with-script-fu \
    --with-cairo-pdf

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

# makeinstall macro won't work here - libexec is overriden
make DESTDIR=%{buildroot} install

# remove rpaths
find %buildroot -type f -print0 | xargs -0 -L 20 chrpath --delete --keepgoing 2>/dev/null || :

%ifos linux
# remove .la files
find %buildroot -name \*.la -exec %__rm -f {} \;
%endif

#
# Plugins and modules change often (grab the executeable ones)
#
echo "%defattr (-, root, root)" > gimp-plugin-files
find %{buildroot}%{_libdir}/gimp/%{lib_api_version} -type f | sed "s@^%{buildroot}@@g" | grep -v '\.a$' >> gimp-plugin-files

# .pyc and .pyo files don't exist yet
grep "\.py$" gimp-plugin-files > gimp-plugin-files-py
for file in $(cat gimp-plugin-files-py); do
    for newfile in ${file}c ${file}o; do
        fgrep -q -x "$newfile" gimp-plugin-files || echo "$newfile"
    done
done >> gimp-plugin-files

%if %{with static}
echo "%defattr (-, root, root)" > gimp-static-files
find %{buildroot}%{_libdir}/gimp/%{lib_api_version} -type f | sed "s@^%{buildroot}@@g" | grep '\.a$' >> gimp-static-files
%endif

#
# Auto detect the lang files.
#
%find_lang gimp%{gettext_version}
%find_lang gimp%{gettext_version}-std-plug-ins
%find_lang gimp%{gettext_version}-script-fu
%find_lang gimp%{gettext_version}-libgimp
%find_lang gimp%{gettext_version}-tips
%find_lang gimp%{gettext_version}-python

cat gimp%{gettext_version}.lang gimp%{gettext_version}-std-plug-ins.lang gimp%{gettext_version}-script-fu.lang gimp%{gettext_version}-libgimp.lang gimp%{gettext_version}-tips.lang gimp%{gettext_version}-python.lang > gimp-all.lang

#
# Build the master filelists generated from the above mess.
#
cat gimp-plugin-files gimp-all.lang > gimp.files

# install convenience symlinks
ln -snf gimp-%{binver} %{buildroot}%{_bindir}/gimp
ln -snf gimp-%{binver}.1 %{buildroot}%{_mandir}/man1/gimp.1
ln -snf gimp-console-%{binver} %{buildroot}/%{_bindir}/gimp-console
ln -snf gimp-console-%{binver}.1 %{buildroot}/%{_mandir}/man1/gimp-console.1
ln -snf gimptool-%{lib_api_version} %{buildroot}%{_bindir}/gimptool
ln -snf gimptool-%{lib_api_version}.1 %{buildroot}%{_mandir}/man1/gimptool.1
ln -snf gimprc-%{binver}.5 %{buildroot}/%{_mandir}/man5/gimprc.5

%clean
rm -rf %{buildroot}

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f gimp.files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc docs/*.xcf*
%{_datadir}/applications/*.desktop

%dir %{_datadir}/gimp
%dir %{_datadir}/gimp/%{lib_api_version}
%{_datadir}/gimp/%{lib_api_version}/dynamics/
%{_datadir}/gimp/%{lib_api_version}/menus/
%{_datadir}/gimp/%{lib_api_version}/tags/
%{_datadir}/gimp/%{lib_api_version}/tips/
%{_datadir}/gimp/%{lib_api_version}/ui/
%dir %{_libdir}/gimp
%dir %{_libdir}/gimp/%{lib_api_version}
%dir %{_libdir}/gimp/%{lib_api_version}/environ
#%dir %{_libdir}/gimp/%{lib_api_version}/fonts
%dir %{_libdir}/gimp/%{lib_api_version}/interpreters
%dir %{_libdir}/gimp/%{lib_api_version}/modules
%dir %{_libdir}/gimp/%{lib_api_version}/plug-ins
%exclude %{_libdir}/gimp/%{lib_api_version}/plug-ins/help-browser
%dir %{_libdir}/gimp/%{lib_api_version}/python
#%dir %{_libdir}/gimp/%{lib_api_version}/tool-plug-ins

%{_datadir}/gimp/%{lib_api_version}/brushes/
%{_datadir}/gimp/%{lib_api_version}/fractalexplorer/
%{_datadir}/gimp/%{lib_api_version}/gfig/
%{_datadir}/gimp/%{lib_api_version}/gflare/
%{_datadir}/gimp/%{lib_api_version}/gimpressionist/
%{_datadir}/gimp/%{lib_api_version}/gradients/
# %{_datadir}/gimp/%{lib_api_version}/help/
%{_datadir}/gimp/%{lib_api_version}/images/
%{_datadir}/gimp/%{lib_api_version}/palettes/
%{_datadir}/gimp/%{lib_api_version}/patterns/
%{_datadir}/gimp/%{lib_api_version}/scripts/
%{_datadir}/gimp/%{lib_api_version}/themes/

%dir %{_sysconfdir}/gimp
%dir %{_sysconfdir}/gimp/%{lib_api_version}
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/controllerrc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/gimprc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/gtkrc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/unitrc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/sessionrc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/templaterc
%config(noreplace) %{_sysconfdir}/gimp/%{lib_api_version}/menurc

%{_bindir}/gimp-%{binver}
%{_bindir}/gimp-console-%{binver}

%{_bindir}/gimp
%{_bindir}/gimp-console

%{_mandir}/man1/gimp-%{binver}.1*
%{_mandir}/man1/gimp-console-%{binver}.1*
%{_mandir}/man5/gimprc-%{binver}.5*

%{_mandir}/man1/gimp.1*
%{_mandir}/man1/gimp-console.1*
%{_mandir}/man5/gimprc.5*

%{_datadir}/icons/hicolor/*/apps/gimp.png

%files libs
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/libgimp-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimp-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpbase-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpbase-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpcolor-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpcolor-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpconfig-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpconfig-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpmath-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpmath-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpmodule-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpmodule-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpthumb-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpthumb-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpui-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpui-%{lib_api_version}.so.%{interface_age}
%{_libdir}/libgimpwidgets-%{lib_api_version}.so.%{interface_age}.%{lib_minor}.%{lib_micro}
%{_libdir}/libgimpwidgets-%{lib_api_version}.so.%{interface_age}

%if %{with static}
%files devel -f gimp-static-files
%else
%files devel
%endif
%defattr (-, root, root, 0755)
%doc HACKING README.i18n
%doc %{_datadir}/gtk-doc

%{_libdir}/*.so
%dir %{_libdir}/gimp
%dir %{_libdir}/gimp/%{lib_api_version}
%dir %{_libdir}/gimp/%{lib_api_version}/modules
%ifnos linux
%{_libdir}/*.la
%{_libdir}/gimp/%{lib_api_version}/modules/*.la
%endif
%{_datadir}/aclocal/*.m4
%{_includedir}/gimp-%{lib_api_version}
%{_libdir}/pkgconfig/*

%files devel-tools
%defattr (-, root, root, 0755)
%{_bindir}/gimptool-%{lib_api_version}
%{_mandir}/man1/gimptool-%{lib_api_version}.1*

%{_bindir}/gimptool
%{_mandir}/man1/gimptool.1*

%files help-browser
%defattr (-, root, root, 0755)
%{_libdir}/gimp/%{lib_api_version}/plug-ins/help-browser

%changelog
* Sun Feb 12 2012 David Peitler <qqroach@riftworks.org> - latest-1
- Fork from official Fedora SRPM.
