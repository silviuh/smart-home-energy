# -*- encoding: utf-8 -*-
# stub: dig_rb 1.0.1 ruby lib

Gem::Specification.new do |s|
  s.name = "dig_rb"
  s.version = "1.0.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib"]
  s.authors = ["Jonathan Rochkind"]
  s.bindir = "exe"
  s.date = "2016-01-21"
  s.email = ["jonathan@dnil.net"]
  s.homepage = "https://github.com/jrochkind/dig_rb"
  s.licenses = ["MIT"]
  s.rubygems_version = "2.4.5.5"
  s.summary = "Array/Hash/Struct#dig backfill for ruby"

  s.installed_by_version = "2.4.5.5" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<rake>, ["~> 10.0"])
      s.add_development_dependency(%q<minitest>, ["~> 5.8.0"])
    else
      s.add_dependency(%q<rake>, ["~> 10.0"])
      s.add_dependency(%q<minitest>, ["~> 5.8.0"])
    end
  else
    s.add_dependency(%q<rake>, ["~> 10.0"])
    s.add_dependency(%q<minitest>, ["~> 5.8.0"])
  end
end
