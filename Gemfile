# frozen_string_literal: true

source "https://rubygems.org"

# Jekyll is the only runtime dependency. Layouts, the feed, the sitemap and the
# tag index are plain Liquid templates in this repository, so no theme gem or
# plugin is needed.
gem "jekyll", "4.4.1"

group :test do
  # Checks the built site for broken internal links and images in CI.
  gem "html-proofer", "5.0.10"
end

# Windows has no system zoneinfo database; Jekyll needs it for `timezone`.
gem "tzinfo-data", platforms: [:windows]
