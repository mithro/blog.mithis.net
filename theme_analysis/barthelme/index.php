<?php get_header() ?>

	<div id="container">
		<div id="content" class="hfeed">

<?php while ( have_posts() ) : the_post() ?>

			<div id="post-<?php the_ID() ?>" class="<?php barthelme_post_class() ?>">
				<div class="post-container">
					<div class="post-content">
						<h2 class="entry-title"><a href="<?php the_permalink() ?>" title="<?php printf(__('Permalink to %s', 'barthelme'), _wp_specialchars(get_the_title(), 1)) ?>" rel="bookmark"><?php the_title() ?></a></h2>
						<div class="entry-content">
<?php the_content('<span class="more-link">'.__('Continue reading &rsaquo;', 'barthelme').'</span>'); ?>

<?php link_pages('<div class="page-link">'.__('Pages: ', 'barthelme'), "</div>\n", 'number'); ?>

<?php the_tags(__('<span class="tag-links">Tagged ', 'barthelme'), ", ", "</span>") ?>

						</div>
					</div>
				</div>
				<div class="entry-meta">
					<span class="entry-date"><abbr class="published" title="<?php the_time('Y-m-d\TH:i:sO'); ?>"><?php unset($previousday); printf(__('%1$s', 'barthelme'), the_date('Y m d', false)) ?></abbr></span>
					<?php barthelme_author_link(); // Displays an author link as selected in the theme options menu ?>
					<span class="entry-category"><?php the_category('<br/>') ?></span>
					<span class="entry-comments"><?php comments_popup_link(__('Comments (0)', 'barthelme'), __('Comments (1)', 'barthelme'), __('Comments (%)', 'barthelme')) ?></span>
					<span class="entry-permalink"><?php printf(__('<a href="%1$s" title="Permalink to %2$s">Permalink</a>', 'barthelme'), get_permalink(), _wp_specialchars(get_the_title(), 'double') ) ?></span>
<?php edit_post_link(__('Edit', 'barthelme'), "\t\t\t\t\t<span class='entry-edit'>", "</span>\n"); ?>
				</div>
			</div><!-- .post -->

<?php endwhile ?>

			<div id="nav-below" class="navigation">
				<div class="nav-previous"><?php next_posts_link(__('&laquo; Older posts', 'barthelme')) ?></div>
				<div class="nav-next"><?php previous_posts_link(__('Newer posts &raquo;', 'barthelme')) ?></div>
			</div>

		</div><!-- #content .hfeed -->
	</div><!-- #container -->

<?php get_sidebar() ?>
<?php get_footer() ?>