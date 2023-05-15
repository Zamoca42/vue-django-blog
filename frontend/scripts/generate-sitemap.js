const { SitemapStream, streamToPromise } = require('sitemap');
const { createWriteStream } = require('fs');
const axios = require('axios');

const links = [
  { url: '/', changefreq: 'daily', priority: 1 },
  { url: '/posts', changefreq: 'daily', priority: 0.7 },
  { url: '/info', changefreq: 'monthly', priority: 0.5 },
];

const sitemap = new SitemapStream({ hostname: 'https://www.zamoca.space' });

axios.get('https:/server.zamoca.space/api2/post/')
  .then(response => {
    const posts = response.data;
    posts.forEach(post => {
      links.push({ url: `/posts/${post.id}`, changefreq: 'weekly', priority: 0.7 });
    });

    sitemap.pipe(createWriteStream('public/sitemap.xml'));

    links.forEach(link => {
      sitemap.write(link);
    });

    sitemap.end();
  })
  .catch(error => {
    console.error('Failed to fetch posts:', error);
  });