module Jekyll
  class FuturePostsGenerator < Generator
    def generate(site)
      posts_path = File.join(site.source, '_posts')
      future_posts = []
      
      Dir.glob(File.join(posts_path, '*.md')).each do |file|
        content = File.read(file)
        
        # Parsear frontmatter
        if content =~ /^---\n(.+?)\n---\n(.*)$/m
          front_matter = $1
          post_content = $2
          
          # Extraer fecha del frontmatter
          if front_matter =~ /date:\s*(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})/
            date = Time.new($1.to_i, $2.to_i, $3.to_i, $4.to_i, $5.to_i, $6.to_i, '+01:00')
            
            # Extraer título
            title = front_matter.match(/title:\s*["']?(.+?)["']?\s*$/m)&.captures&.first || 'Untitled'
            
            # Extraer excerpt
            excerpt = front_matter.match(/excerpt:\s*["']?(.+?)["']?\s*$/m)&.captures&.first
            
            # Extraer expires
            expires = nil
            if front_matter =~ /expires:\s*(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})/
              expires = Time.new($1.to_i, $2.to_i, $3.to_i, $4.to_i, $5.to_i, $6.to_i, '+01:00')
            end
            
            future_posts << {
              'title' => title,
              'date' => date,
              'excerpt' => excerpt,
              'expires' => expires,
              'file' => File.basename(file)
            }
          end
        end
      end
      
      # Agregar future_posts al sitio
      site.config['future_posts'] = future_posts.sort_by { |p| p['date'] }.reverse
    end
  end
end
