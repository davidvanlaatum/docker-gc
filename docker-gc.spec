%undefine _missing_build_ids_terminate_build

Name:           docker-gc
Version:        1.0.0
Release:        1%{?dist}
Summary:        Docker Garbage Collector
URL:            https://github.com/davidvanlaatum/docker-gc
Source0:        docker-gc-%{version}.tar.gz

BuildRequires:  gcc

BuildRequires:  golang >= 1.2-7

# pull in golang libraries by explicit import path, inside the meta golang()
#BuildRequires:  golang(github.com/fsouza/go-dockerclient)
#BuildRequires:  golang(github.com/sirupsen/logrus)
#BuildRequires:  golang(github.com/boltdb/bolt)

%{?systemd_requires}
BuildRequires: systemd

%description

%prep
%setup -q -n docker-gc-%{version}

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build/src/github.com/davidvanlaatum
ln -s $(pwd) ./_build/src/github.com/davidvanlaatum/docker-gc

export GOPATH=$(pwd)/_build:%{gopath} CGO_ENABLED=1
go get -d -v
go build -o docker-gc .

%install
install -d %{buildroot}%{_sbindir}
install -p -m 0755 ./docker-gc %{buildroot}%{_sbindir}/docker-gc
install -D -m 0644 ./docker-gc.service %{buildroot}%{_unitdir}/docker-gc.service

%post
%systemd_post docker-gc.service

%preun
%systemd_preun docker-gc.service

%postun
%systemd_postun_with_restart docker-gc.service

%files
%defattr(-,root,root,-)
%{_sbindir}/docker-gc
%{_unitdir}/docker-gc.service

%changelog

