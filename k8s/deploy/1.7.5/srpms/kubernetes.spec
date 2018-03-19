%global KUBE_VERSION 1.7.5
%global CNI_RELEASE 0.6.0
%global RPM_RELEASE 1
%global ARCH amd64

Name: kubernetes
Version: %{KUBE_VERSION}
Release: %{RPM_RELEASE}
Summary: Container cluster management
License: ASL 2.0

URL: https://kubernetes.io
Source0: https://dl.k8s.io/v%{KUBE_VERSION}/bin/linux/%{ARCH}/kubelet
Source1: kubelet.service
Source2: https://dl.k8s.io/v%{KUBE_VERSION}/bin/linux/%{ARCH}/kubectl
Source3: https://dl.k8s.io/v%{KUBE_VERSION}/bin/linux/%{ARCH}/kube-apiserver
Source4: https://dl.k8s.io/v%{KUBE_VERSION}/bin/linux/%{ARCH}/kube-scheduler
Source4: https://dl.k8s.io/v%{KUBE_VERSION}/bin/linux/%{ARCH}/kube-controller-manager
Source5: https://github.com/containernetworking/plugins/releases/download/v%{CNI_RELEASE}/cni-plugins-%{ARCH}-v%{CNI_RELEASE}.tgz
Source6: 10-kubeadm.conf

BuildRequires: curl
Requires: iptables >= 1.4.21
Requires: kubernetes-cni >= 0.6.0
Requires: socat
Requires: util-linux
Requires: ethtool
Requires: iproute
Requires: ebtables

%description
The Kubernetes, the container cluster manager.


%package -n kube-apiserver

Version: %{KUBE_RELEASE}
Release: %{RPM_RELEASE}
Summary: kube-apiserver pkg

%description -n kube-apiserver
The kube-apiserver of k8s

%package -n kube-scheduler

Version: %{KUBE_RELEASE}
Release: %{RPM_RELEASE}
Summary: kube-scheduler pkg

%description -n kube-scheduler
The kube-scheduler of k8s


%package -n kube-controller-manager

Version: %{KUBE_RELEASE}
Release: %{RPM_RELEASE}
Summary: kube-controller-manager pkg

%description -n kube-controller-manager
The kube-controller-manager of k8s


%package -n kubernetes-cni

Version: 0.6.0
Release: %{RPM_RELEASE}
Summary: Binaries required to provision kubernetes container networking
Requires: kubelet

%description -n kubernetes-cni
Binaries required to provision container networking.

%package -n kubectl

Version: %{KUBE_VERSION}
Release: %{RPM_RELEASE}
Summary: Command-line utility for interacting with a Kubernetes cluster.

%description -n kubectl
Command-line utility for interacting with a Kubernetes cluster.


%prep
# Assumes the builder has overridden sourcedir to point to directory
# with this spec file. (where these files are stored) Copy them into
# the builddir so they can be installed.
# This is a useful hack for faster Docker builds when working on the spec or
# with locally obtained sources.
#
# Example:
#   spectool -gf kubelet.spec
#   rpmbuild --define "_sourcedir $PWD" -bb kubelet.spec
#

cp -p %SOURCE0 %{_builddir}/
cp -p %SOURCE1 %{_builddir}/
cp -p %SOURCE2 %{_builddir}/
cp -p %SOURCE3 %{_builddir}/
cp -p %SOURCE4 %{_builddir}/
cp -p %SOURCE5 %{_builddir}/
%setup -D -T -a 6 -n %{_builddir}/


%install

install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/systemd/system/
install -m 755 -d %{buildroot}%{_sysconfdir}/systemd/system/kubelet.service.d/
install -m 755 -d %{buildroot}%{_sysconfdir}/cni/net.d/
install -m 755 -d %{buildroot}%{_sysconfdir}/kubernetes/manifests/
install -m 755 -d %{buildroot}/var/lib/kubelet/
install -p -m 755 -t %{buildroot}%{_bindir}/ kubelet
install -p -m 755 -t %{buildroot}%{_bindir}/ kubectl
install -p -m 755 -t %{buildroot}%{_bindir}/ kube-apiserver
install -p -m 755 -t %{buildroot}%{_bindir}/ kube-scheduler
install -p -m 755 -t %{buildroot}%{_bindir}/ kube-controller-manager
install -p -m 755 -t %{buildroot}%{_sysconfdir}/systemd/system/ kubelet.service
install -p -m 755 -t %{buildroot}%{_sysconfdir}/systemd/system/kubelet.service.d/ 10-kubeadm.conf


install -m 755 -d %{buildroot}/opt/cni
# bin directory from cni-amd64-%{CNI_RELEASE}.tar.gz with a list of cni plugins (among other things)
mv bin/ %{buildroot}/opt/cni/


%files
%{_bindir}/kubelet
%{_sysconfdir}/systemd/system/kubelet.service
%{_sysconfdir}/kubernetes/manifests/

%files -n kubernetes-cni
/opt/cni

%files -n kubectl
%{_bindir}/kubectl

%files -n kubeadm
%{_bindir}/kubeadm
%{_sysconfdir}/systemd/system/kubelet.service.d/10-kubeadm.conf

%doc


%changelog
* Thu Aug 3 2017 Jacob Beacham <beacham@google.com> - 1.7.3
- Bump version of kubelet and kubectl to v1.7.3.

* Wed Jul 26 2017 Jacob Beacham <beacham@google.com> - 1.7.2
- Bump version of kubelet and kubectl to v1.7.2.

* Fri Jul 14 2017 Jacob Beacham <beacham@google.com> - 1.7.1
- Bump version of kubelet and kubectl to v1.7.1.

* Mon Jun 30 2017 Mike Danese <mikedanese@google.com> - 1.7.0
- Bump version of kubelet and kubectl to v1.7.0.

* Fri May 19 2017 Jacob Beacham <beacham@google.com> - 1.6.4
- Bump version of kubelet and kubectl to v1.6.4.

* Wed May 10 2017 Jacob Beacham <beacham@google.com> - 1.6.3
- Bump version of kubelet and kubectl to v1.6.3.

* Wed Apr 26 2017 Jacob Beacham <beacham@google.com> - 1.6.2
- Bump version of kubelet and kubectl to v1.6.2.

* Mon Apr 3 2017 Mike Danese <mikedanese@google.com> - 1.6.1
- Bump version of kubelet and kubectl to v1.6.1.

* Tue Mar 28 2017 Lucas Käldström <lucas.kaldstrom@hotmail.co.uk>
- Bump CNI version to v0.5.1.

* Wed Mar 15 2017 Lucas Käldström <lucas.kaldstrom@hotmail.co.uk> - 1.6.0
- Bump version of kubelet, kubectl and kubeadm to v1.6.0.

* Tue Dec 13 2016 Mike Danese <mikedanese@google.com> - 1.5.4
- Bump version of kubelet and kubectl to v1.5.4.

* Tue Dec 13 2016 Lucas Käldström <lucas.kaldstrom@hotmail.co.uk> - 1.5.1
- Bump version of kubelet and kubectl to v1.5.1, plus kubeadm to the third stable version

* Tue Dec 6 2016 Lucas Käldström <lucas.kaldstrom@hotmail.co.uk> - 1.5.0-beta.2
- Bump version of kubelet and kubectl

* Wed Nov 16 2016 Alexander Kanevskiy <alexander.kanevskiy@intel.com>
- fix iproute and mount dependencies (#204)

* Sun Nov 6 2016 Lucas Käldström <lucas.kaldstrom@hotmail.co.uk>
- Sync the debs and rpm files; add some kubelet dependencies to the rpm manifest

* Wed Nov 2 2016 Lucas Käldström <lucas.kaldstrom@hotmail.co.uk>
- Bump version of kubeadm to v1.5.0-alpha.2.380+85fe0f1aadf91e

* Fri Oct 21 2016 Ilya Dmitrichenko <errordeveloper@gmail.com> - 1.4.4-0
- Bump version of kubelet and kubectl

* Mon Oct 17 2016 Lucas Käldström <lucas.kaldstrom@hotmail.co.uk> - 1.4.3-0
- Bump version of kubeadm

* Fri Oct 14 2016 Matthew Mosesohn  <mmosesohn@mirantis.com> - 1.4.0-1
- Allow locally built/previously downloaded binaries

* Tue Sep 20 2016 dgoodwin <dgoodwin@redhat.com> - 1.4.0-0
- Add kubectl and kubeadm sub-packages.
- Rename to kubernetes-cni.
- Update versions of CNI.

* Wed Jul 20 2016 dgoodwin <dgoodwin@redhat.com> - 1.3.4-1
- Initial packaging.