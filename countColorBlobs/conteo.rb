#!/usr/bin/env ruby

raw = File.read ARGV[0]

rows = raw.split("\n").map { |l| l.split(', ') }

groups = rows.group_by { |r| r[0] }

summary = groups.map { |k,v|
  k + " ->>> " + v.map{ |e| e[2].to_i }.reduce(&:+).to_s
}

puts summary
