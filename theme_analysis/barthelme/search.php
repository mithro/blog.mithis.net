<?php get_header() ?>

	<div id="container">
		<div id="content" class="hfeed">

<?php if (have_posts()) : ?>

		<h2 class="page-title"><span class="archive-meta"><span class="meta-sep">{</span> <?php printf(__('&#8220;%1$s&#8221;', 'barthelme'), the_search_query() ); ?> <span class="meta-sep">}</span></span> <?php _e('Search Results', 'barthelme') ?></h2>

<?php while (have_posts()) : the_post(); ?>

			<div id="post-<?php the_ID() ?>" class="<?php barthelme_post_class() ?>">
				<div class="post-container">
					<div class="post-content">
						<h3 class="entry-title"><a href="<?php the_permalink() ?>" title="<?php printf(__('Permalink to %s', 'barthelme'), _wp_specialchars(get_the_title(), 1)) ?>" rel="bookmark"><?php the_title() ?></a></h3>
						<div class="entry-content">
<?php the_content('<span class="more-link">'.__('Continue reading &rsaquo;', 'barthelme').'</span>'); ?>

<?php the_tags(__('<span class="tag-links">Tagged ', 'barthelme'), ", ", "</span>") ?>

						</div>
					</div>
				</div>
				<div class="entry-meta">
					<span class="entry-date"><abbr class="published" title="<?php the_time('Y-m-d\TH:i:sO'); ?>"><?php unset($previousday); printf(__('%1$s', 'barthelme'), the_date('Y m d', false)) ?></abbr></span>
					<?php barthelme_author_link(); ?>
					<span class="entry-comments"><?php comments_popup_link(__('Comments (0)', 'barthelme'), __('Comments (1)', 'barthelme'), __('Comments (%)', 'barthelme')) ?></span>
<?php edit_post_link(__('Edit', 'barthelme'), "\t\t\t\t\t<span class='entry-edit'>", "</span>\n"); ?>
				</div>
			</div><!-- .post -->

<?php endwhile; ?>

			<div id="nav-below" class="navigation">
				<div class="nav-previous"><?php next_posts_link(__('&laquo; Older posts', 'barthelme')) ?></div>
				<div class="nav-next"><?php previous_posts_link(__('Newer posts &raquo;', 'barthelme')) ?></div>
			</div>

<?php else : ?>

		<h2 class="page-title"><span class="search-meta"><span class="meta-sep">{</span> <?php printf(__('&#8220;%1$s&#8221;', 'barthelme'), _wp_specialchars(stripslashes($_GET['s']), true) ); ?> <span class="meta-sep">}</span></span> <?php _e('Search Results', 'barthelme') ?></h2>

			<div id="post-0" class="post">
				<h3 class="entry-title"><?php _e('Nothing Found', 'barthelme') ?></h3>
				<div class="entry-content">
					<p><?php _e('Sorry, but nothing matched your search criteria. Please try again with some different keywords.', 'barthelme') ?></p>
				</div>
				<form id="noresults-searchform" method="get" action="<?php bloginfo('home') ?>">
					<div>
						<input id="noresults-s" name="s" type="text" value="<?php the_search_query() ?>" size="40" />
						<input id="noresults-searchsubmit" name="searchsubmit" type="submit" value="<?php _e('Search', 'barthelme') ?>" />
					</div>
				</form>
			</div><!-- .post #post-0 -->

<?php endif; ?>

		</div><!-- #content .hfeed -->
	</div><!-- #container -->

<?php get_sidebar() ?>
<?php get_footer() ?>