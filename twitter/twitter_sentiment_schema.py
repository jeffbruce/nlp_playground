create_query = '''
create table if not exists tweets (
	tweet_id bigint primary key,
	user_id bigint not null,
	created_at timestamp,
	search_term varchar(128),
	text varchar(512)
);
'''

drop_query = '''
drop table if exists tweets;
'''

insert_query = '''
insert into tweets (tweet_id, user_id, created_at, search_term, text) values (3, 1, '2018-02-02 00:00:00', 'bitcoin', 'bitcoin is done');
'''

upsert_query = '''
insert into tweets (tweet_id, user_id, created_at, search_term, text)
values (4, 1, '2018-02-02 00:00:00', 'bitcoin', 'bitcoin is done'), (5, 1, '2019-03-01 00:00:00', 'ethereum', 'ethereum is fo real'), (2, 1, '2019-03-01 00:00:00', 'ethereum', 'bitcoin is now ethereum')
on conflict (tweet_id) do update
set user_id = excluded.user_id,
		created_at = excluded.created_at,
		search_term = excluded.search_term,
		text = excluded.text;
'''

select_query = '''select * from
tweets;'''