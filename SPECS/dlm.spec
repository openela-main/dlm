Name:           dlm
Version:        4.2.0
Release:        2%{?dist}
License:        GPLv2 and GPLv2+ and LGPLv2+
# For a breakdown of the licensing, see README.license
Summary:        dlm control daemon and tool
URL:            https://pagure.io/dlm
BuildRequires:  gcc
BuildRequires:  glibc-kernheaders
BuildRequires:  corosynclib-devel >= 3.1.0
BuildRequires:  pacemaker-libs-devel >= 1.1.7
BuildRequires:  libxml2-devel
BuildRequires:  systemd-units
BuildRequires:  systemd-devel
BuildRequires: make
Source0:	https://releases.pagure.org/dlm/%{name}-%{version}.tar.gz

Patch0: 0001-Revert-treewide-add-fcf-protection-full-to-CFLAGS.patch

%if 0%{?rhel} && 0%{?rhel} <= 7
ExclusiveArch: i686 x86_64
%endif

Requires:       %{name}-lib = %{version}-%{release}
Requires:       corosync >= 3.1.0
%{?fedora:Requires: kernel-modules-extra}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Conflicts: cman

%description
The kernel dlm requires a user daemon to control membership.

%prep
%setup -q
%patch0 -p1 -b .backup0

%build
# upstream does not require configure
# upstream does not support _smp_mflags
CFLAGS=$RPM_OPT_FLAGS make
CFLAGS=$RPM_OPT_FLAGS make -C fence

%install
rm -rf $RPM_BUILD_ROOT
make install LIBDIR=%{_libdir} DESTDIR=$RPM_BUILD_ROOT
make -C fence install LIBDIR=%{_libdir} DESTDIR=$RPM_BUILD_ROOT

install -Dm 0644 init/dlm.service %{buildroot}%{_unitdir}/dlm.service
install -Dm 0644 init/dlm.sysconfig %{buildroot}/etc/sysconfig/dlm

%post
%systemd_post dlm.service

%preun
%systemd_preun dlm.service

%postun
%systemd_postun_with_restart dlm.service

%files
%doc README.license
%{_unitdir}/dlm.service
%{_sbindir}/dlm_controld
%{_sbindir}/dlm_tool
%{_sbindir}/dlm_stonith
%{_mandir}/man8/dlm*
%{_mandir}/man5/dlm*
%{_mandir}/man3/*dlm*
%config(noreplace) %{_sysconfdir}/sysconfig/dlm

%package        lib
Summary:        Library for %{name}
Conflicts:      clusterlib

%description    lib
The %{name}-lib package contains the libraries needed to use the dlm
from userland applications.

%ldconfig_scriptlets lib

%files          lib
/usr/lib/udev/rules.d/*-dlm.rules
%{_libdir}/libdlm*.so.*

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-lib = %{version}-%{release}
Conflicts:      clusterlib-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files          devel
%{_libdir}/libdlm*.so
%{_includedir}/libdlm*.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 14 2022 David Teigland <teigland@redhat.com> - 4.2.0-2
- rebuild with tests

* Wed Oct 12 2022 David Teigland <teigland@redhat.com> - 4.2.0-1
- new upstream version

* Tue Feb 15 2022 David Teigland <teigland@redhat.com> - 4.1.1-2
- compiler warnings and makefile flags

* Mon Nov 15 2021 David Teigland <teigland@redhat.com> - 4.1.1-1
- new upstream version

* Wed Aug 25 2021 David Teigland <teigland@redhat.com> - 4.0.9-7
- fix pacemaker header

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 4.0.9-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 4.0.9-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 31 2019 David Teigland <teigland@redhat.com> - 4.0.9-1
- New upstream realease

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Mar 24 2018 Richard W.M. Jones <rjones@redhat.com> - 4.0.6-8
- Fixes for glibc 2.27, required for riscv64.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 10 2017 Troy Dawson <tdawson@redhat.com> - 4.0.6-5
- Cleanup spec file conditionals

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jun 10 2016 David Teigland <teigland@redhat.com> - 4.0.6-2
- try fixing broken libsystemd

* Fri Jun 10 2016 David Teigland <teigland@redhat.com> - 4.0.6-1
- New upstream release

* Tue Apr 26 2016 David Teigland <teigland@redhat.com> - 4.0.5-1
- New upstream release

* Mon Feb 22 2016 David Teigland <teigland@redhat.com> - 4.0.4-1
- New upstream release dlm-4.0.4

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 David Teigland <teigland@redhat.com> - 4.0.1-1
- New usptream release, fencing fixes

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 David Teigland <teigland@redhat.com> - 4.0.0-1
- New upstream release, systemd fixes

* Wed Sep 05 2012 Václav Pavlín <vpavlin@redhat.com> - 3.99.5-7
- Scriptlets replaced with new systemd macros (#850093)

* Tue Aug 28 2012 David Teigland <teigland@redhat.com> - 3.99.5-6
- only fedora requires kernel-modules-extra

* Thu Aug 16 2012 David Teigland <teigland@redhat.com> - 3.99.5-5
- dlm_controld: remove fence_all from cli

* Thu Aug 16 2012 David Teigland <teigland@redhat.com> - 3.99.5-4
- dlm_stonith: include errno.h

* Thu Aug 16 2012 David Teigland <teigland@redhat.com> - 3.99.5-3
- dlm_controld: fix uninitialized mem for fence_all config

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.99.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 David Teigland <teigland@redhat.com> - 3.99.5-1
- New upstream release

* Wed May 30 2012 David Teigland <teigland@redhat.com> - 3.99.4-2
- Limit rhel arches

* Mon May 21 2012 David Teigland <teigland@redhat.com> - 3.99.4-1
- New upstream release

* Mon May 14 2012 David Teigland <teigland@redhat.com> - 3.99.3-1
- New upstream release

* Wed Apr 11 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.2-1
- New upstream release

* Thu Mar 29 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.1-4
- Merge back from F17

* Wed Mar 21 2012 David Teigland <teigland@redhat.com> - 3.99.1-3
- Fix dlm_stonith linking

* Wed Mar 21 2012 David Teigland <teigland@redhat.com> - 3.99.1-2
- Require pacemaker-libs-devel to build dlm_stonith

* Wed Mar 21 2012 David Teigland <teigland@redhat.com> - 3.99.1-1
- Update to 3.99.1

* Fri Mar 16 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.0-8
- Rebuild against new corosync (soname change).

* Thu Feb 16 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.0-7
- Update to upstream HEAD 2ad89c869git.
- Bump BuildRequires and Requires to new corosync

* Mon Feb 13 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.0-6
- Fix init/systemd service to use /etc/sysconfig/dlm

* Mon Feb  6 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.0-5
- Fix systemd service to recognize /etc/sysconfig/dlm_controld

* Fri Feb  3 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.0-4
- Fix systemd service to modprobe dlm

* Fri Feb  3 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.0-3
- Add patch to fix udev rules and make sure dlm_controld can find
  its devices

* Thu Feb  2 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.99.0-2
- Add Conflicts with clusterlib/cman as necessary

* Tue Jan 24 2012 David Teigland <teigland@redhat.com> - 3.99.0-1
- initial package

