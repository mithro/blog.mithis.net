<?php get_header(); ?>

	<div id="container">
		<div id="content" class="hfeed">

<?php the_post() ?>

			<div id="post-<?php the_ID(); ?>" class="<?php barthelme_post_class(); ?>">
				<div class="entry-date">{ <abbr class="published" title="<?php the_time('Y-m-d\TH:i:sO'); ?>"><?php unset($previousday); printf(__('%1$s', 'barthelme'), the_date('Y m d', false)) ?></abbr> }</div>
				<h2 class="entry-title"><?php the_title(); ?></h2>
				<h3 class="page-title"><span>From</span> <a href="<?php echo get_permalink($post->post_parent) ?>" rev="attachment"><?php echo get_the_title($post->post_parent) ?></a></h3>
				<div class="entry-content">
					<div class="entry-attachment"><a href="<?php echo wp_get_attachment_url($post->ID); ?>" title="<?php echo _wp_specialchars( get_the_title($post->ID), 1 ) ?>" rel="attachment"><?php echo wp_get_attachment_image( $post->ID, 'large' ); ?></a></div>
					<div class="entry-caption"><?php if ( !empty($post->post_excerpt) ) the_excerpt(); ?></div>
<?php the_content('<span class="more-link">'.__('Continue reading &rsaquo;', 'barthelme').'</span>'); ?>

<?php edit_post_link(__('Edit this entry.', 'barthelme'),'<p class="entry-edit">','</p>') ?>

				</div>
				<div id="nav-images" class="navigation">
					<div class="nav-previous"><?php previous_image_link() ?></div>
					<div class="nav-next"><?php next_image_link() ?></div>
				</div>
				<div class="entry-meta">
					<?php printf(__('<span class="entry-published">Posted by %1$s on <abbr class="published" title="%2$sT%3$s">%4$s at %5$s</abbr>.</span> <span class="entry-rsslink">Follow any responses to this post with its <a href="%6$s" title="Comments RSS to %7$s" rel="alternate" type="application/rss+xml">comments RSS</a> feed.</span>', 'barthelme'),
						barthelme_author_link(),
						get_the_time('Y-m-d'),
						get_the_time('H:i:sO'),
						get_the_time('l, F j, Y,'),
						get_the_time(),
						esc_url( get_post_comments_feed_link() ),
						_wp_specialchars(get_the_title(), 'double') ) ?>

<?php if (('open' == $post-> comment_status) && ('open' == $post->ping_status)) : ?>
					<span class="entry-interact"><?php printf(__('You can <a href="#respond" title="Post a comment">post a comment</a> or <a href="%s" rel="trackback" title="Trackback URL for your post">trackback</a> from your blog.', 'barthelme'), get_trackback_url()) ?></span>
<?php elseif (!('open' == $post-> comment_status) && ('open' == $post->ping_status)) : ?>
					<span class="entry-interact"><?php printf(__('Comments are closed, but you can <a href="%s" rel="trackback" title="Trackback URL for your post">trackback</a> from your blog.', 'barthelme'), get_trackback_url()) ?></span>
<?php elseif (('open' == $post-> comment_status) && !('open' == $post->ping_status)) : ?>
					<span class="entry-interact"><?php printf(__('You can <a href="#respond" title="Post a comment">post a comment</a>, but trackbacks are closed.', 'barthelme')) ?></span>
<?php elseif (!('open' == $post-> comment_status) && !('open' == $post->ping_status)) : ?>
					<span class="entry-interact"><?php _e('Both comments and trackbacks are currently closed.', 'barthelme') ?></span>
<?php endif; ?>
<?php edit_post_link(__('Edit', 'barthelme'), "\t\t\t\t\t<span class='entry-edit'>", "</span>\n"); ?>
				</div>
			</div>

<?php comments_template() ?>

		</div><!-- #content .hfeed -->
	</div><!-- #container -->

<?php get_sidebar() ?>
<?php get_footer() ?>