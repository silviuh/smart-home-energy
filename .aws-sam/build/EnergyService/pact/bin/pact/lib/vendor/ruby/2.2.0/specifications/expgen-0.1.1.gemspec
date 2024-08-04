# -*- encoding: utf-8 -*-
# stub: expgen 0.1.1 ruby lib

Gem::Specification.new do |s|
  s.name = "expgen"
  s.version = "0.1.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib"]
  s.authors = ["Jonas Nicklas"]
  s.date = "2013-04-02"
  s.description = "Generate random strings from regular expression"
  s.email = ["jonas.nicklas@gmail.com"]
  s.executables = ["expgen"]
  s.files = ["bin/expgen"]
  s.homepage = ""
  s.rubygems_version = "2.4.5.5"
  s.summary = "Generate random regular expression"

  s.installed_by_version = "2.4.5.5" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 3

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_runtime_dependency(%q<parslet>, [">= 0"])
      s.add_development_dependency(%q<pry>, [">= 0"])
      s.add_development_dependency(%q<rspec>, [">= 0"])
    else
      s.add_dependency(%q<parslet>, [">= 0"])
      s.add_dependency(%q<pry>, [">= 0"])
      s.add_dependency(%q<rspec>, [">= 0"])
    end
  else
    s.add_dependency(%q<parslet>, [">= 0"])
    s.add_dependency(%q<pry>, [">= 0"])
    s.add_dependency(%q<rspec>, [">= 0"])
  end
end
