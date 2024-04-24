PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	first_name VARCHAR(20) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(60), 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO user VALUES(1,'jeffrey','jeffreyroh2002@gmail.com',X'24326224313224734c64786455784a6b6768504f46584e326b4c7372755a354a6157416b2e53535962624c58304b59565257786541612e586856736d');
INSERT INTO user VALUES(2,'j','a@gmail.com',X'243262243132247553325543436e7863764f493564372f42685377314f6f354d6c782e30797043534859332f55687755515238647542626174654469');
CREATE TABLE audio_file (
	id INTEGER NOT NULL, 
	audio_name VARCHAR(50) NOT NULL, 
	file_path VARCHAR(100) NOT NULL, 
	genre TEXT NOT NULL, 
	mood TEXT NOT NULL, 
	vocal TEXT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO audio_file VALUES(1,'ES_Another Life.wav_1.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Another Life.wav_1.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 1.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.35, "Relaxed": 0.6}','{"Smooth": 0.2, "Dreamy": 0.8, "Raspy": 0.0, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(2,'ES_Big Open Sky Flyer.wav_2.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Big Open Sky Flyer.wav_2.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.25, "Electronic": 0.0, "Jazz": 0.15, "Korean Ballad": 0.55, "R&B/Soul": 0.05}','{"Emotional": 0.35, "Tense": 0.0, "Bright": 0.05, "Relaxed": 0.6}','{"Smooth": 0.0, "Dreamy": 0.95, "Raspy": 0.05, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(3,'ES_Blue Texas.wav_3.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Blue Texas.wav_3.wav','{"Rock": 0.9, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.9, "Bright": 0.1, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(4,'ES_Bright Red Lights.wav_5.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Bright Red Lights.wav_5.wav','{"Rock": 0.7, "Hip Hop": 0.15, "Pop Ballad": 0.05, "Electronic": 0.1, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.3, "Tense": 0.05, "Bright": 0.65, "Relaxed": 0.0}','{"Smooth": 0.7, "Dreamy": 0.0, "Raspy": 0.15, "Voiceless": 0.15}');
INSERT INTO audio_file VALUES(5,'ES_Can''t Help It.wav_6.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Can''t Help It.wav_6.wav','{"Rock": 0.15, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.7, "Jazz": 0.05, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.95, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.45, "Raspy": 0.2, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(6,'ES_Can''t Stop.wav_7.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Can''t Stop.wav_7.wav','{"Rock": 0.15, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.7, "Jazz": 0.05, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.95, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.45, "Raspy": 0.2, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(7,'ES_Castle to Ruin.wav_8.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Castle to Ruin.wav_8.wav','{"Rock": 0.45, "Hip Hop": 0.0, "Pop Ballad": 0.3, "Electronic": 0.25, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.6, "Bright": 0.4, "Relaxed": 0.0}','{"Smooth": 0.15, "Dreamy": 0.45, "Raspy": 0.15, "Voiceless": 0.25}');
INSERT INTO audio_file VALUES(8,'ES_Do Over.wav_9.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Do Over.wav_9.wav','{"Rock": 0.0, "Hip Hop": 0.05, "Pop Ballad": 0.1, "Electronic": 0.4, "Jazz": 0.3, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.35, "Tense": 0.0, "Bright": 0.2, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(9,'ES_Eyes in the Back of My Head.wav_10.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Eyes in the Back of My Head.wav_10.wav','{"Rock": 0.0, "Hip Hop": 0.85, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.25, "Tense": 0.4, "Bright": 0.35, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.4, "Raspy": 0.2, "Voiceless": 0.05}');
INSERT INTO audio_file VALUES(10,'ES_Good Vibes Only.wav_11.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Good Vibes Only.wav_11.wav','{"Rock": 0.0, "Hip Hop": 0.8, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.2}','{"Emotional": 0.0, "Tense": 0.15, "Bright": 0.4, "Relaxed": 0.45}','{"Smooth": 0.2, "Dreamy": 0.0, "Raspy": 0.8, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(11,'ES_Hierarchy.wav_12.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Hierarchy.wav_12.wav','{"Rock": 1.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.6, "Bright": 0.4, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.3, "Raspy": 0.65, "Voiceless": 0.05}');
INSERT INTO audio_file VALUES(12,'ES_I Got Love.wav_13.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_I Got Love.wav_13.wav','{"Rock": 0.6, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.3}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.5, "Dreamy": 0.35, "Raspy": 0.15, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(13,'ES_Lily My Dear.wav_14.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Lily My Dear.wav_14.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 1.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.55, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(14,'ES_Our Song.wav_15.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Our Song.wav_15.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.1, "Electronic": 0.25, "Jazz": 0.0, "Korean Ballad": 0.6, "R&B/Soul": 0.05}','{"Emotional": 1.0, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 1.0, "Raspy": 0.0, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(15,'ES_Paper Crane.wav_16.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Paper Crane.wav_16.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 1.0}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.4, "Dreamy": 0.0, "Raspy": 0.6, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(16,'ES_Roundtrip.wav_17.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Roundtrip.wav_17.wav','{"Rock": 0.75, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.1, "Jazz": 0.15, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.2, "Bright": 0.8, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(17,'ES_Step on That Toe.wav_19.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Step on That Toe.wav_19.wav','{"Rock": 0.4, "Hip Hop": 0.0, "Pop Ballad": 0.1, "Electronic": 0.0, "Jazz": 0.5, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.05, "Tense": 0.1, "Bright": 0.4, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(18,'ES_There''s a Heatwave.wav_20.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_There''s a Heatwave.wav_20.wav','{"Rock": 0.0, "Hip Hop": 0.1, "Pop Ballad": 0.05, "Electronic": 0.7, "Jazz": 0.0, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.2, "Dreamy": 0.6, "Raspy": 0.05, "Voiceless": 0.15}');
INSERT INTO audio_file VALUES(19,'ES_Top Speed.wav_21.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Top Speed.wav_21.wav','{"Rock": 0.0, "Hip Hop": 0.9, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.1}','{"Emotional": 0.4, "Tense": 0.1, "Bright": 0.3, "Relaxed": 0.2}','{"Smooth": 0.3, "Dreamy": 0.4, "Raspy": 0.2, "Voiceless": 0.1}');
INSERT INTO audio_file VALUES(20,'ES_Where R U_.wav_22.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Where R U_.wav_22.wav','{"Rock": 0.0, "Hip Hop": 0.2, "Pop Ballad": 0.0, "Electronic": 0.05, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.75}','{"Emotional": 0.05, "Tense": 0.6, "Bright": 0.35, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.6, "Raspy": 0.05, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(21,'ES_Whispering Love.wav_23.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_Whispering Love.wav_23.wav','{"Rock": 0.05, "Hip Hop": 0.45, "Pop Ballad": 0.0, "Electronic": 0.35, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.05}','{"Emotional": 0.0, "Tense": 0.25, "Bright": 0.7, "Relaxed": 0.05}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(22,'ES_save yourself.wav_18.wav','../data_preprocessing/audio_split/audio_full_mix_split/ES_save yourself.wav_18.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.1, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.8}','{"Emotional": 0.1, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.9}','{"Smooth": 0.05, "Dreamy": 0.8, "Raspy": 0.05, "Voiceless": 0.1}');
INSERT INTO audio_file VALUES(23,'ES_Another Life.wav_1.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Another Life.wav_1.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 1.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.35, "Relaxed": 0.6}','{"Smooth": 0.2, "Dreamy": 0.8, "Raspy": 0.0, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(24,'ES_Big Open Sky Flyer.wav_2.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Big Open Sky Flyer.wav_2.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.25, "Electronic": 0.0, "Jazz": 0.15, "Korean Ballad": 0.55, "R&B/Soul": 0.05}','{"Emotional": 0.35, "Tense": 0.0, "Bright": 0.05, "Relaxed": 0.6}','{"Smooth": 0.0, "Dreamy": 0.95, "Raspy": 0.05, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(25,'ES_Blue Texas.wav_3.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Blue Texas.wav_3.wav','{"Rock": 0.9, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.9, "Bright": 0.1, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(26,'ES_Bright Red Lights.wav_5.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Bright Red Lights.wav_5.wav','{"Rock": 0.7, "Hip Hop": 0.15, "Pop Ballad": 0.05, "Electronic": 0.1, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.3, "Tense": 0.05, "Bright": 0.65, "Relaxed": 0.0}','{"Smooth": 0.7, "Dreamy": 0.0, "Raspy": 0.15, "Voiceless": 0.15}');
INSERT INTO audio_file VALUES(27,'ES_Can''t Help It.wav_6.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Can''t Help It.wav_6.wav','{"Rock": 0.15, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.7, "Jazz": 0.05, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.95, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.45, "Raspy": 0.2, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(28,'ES_Can''t Stop.wav_7.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Can''t Stop.wav_7.wav','{"Rock": 0.15, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.7, "Jazz": 0.05, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.95, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.45, "Raspy": 0.2, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(29,'ES_Castle to Ruin.wav_8.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Castle to Ruin.wav_8.wav','{"Rock": 0.45, "Hip Hop": 0.0, "Pop Ballad": 0.3, "Electronic": 0.25, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.6, "Bright": 0.4, "Relaxed": 0.0}','{"Smooth": 0.15, "Dreamy": 0.45, "Raspy": 0.15, "Voiceless": 0.25}');
INSERT INTO audio_file VALUES(30,'ES_Do Over.wav_9.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Do Over.wav_9.wav','{"Rock": 0.0, "Hip Hop": 0.05, "Pop Ballad": 0.1, "Electronic": 0.4, "Jazz": 0.3, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.35, "Tense": 0.0, "Bright": 0.2, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(31,'ES_Eyes in the Back of My Head.wav_10.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Eyes in the Back of My Head.wav_10.wav','{"Rock": 0.0, "Hip Hop": 0.85, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.25, "Tense": 0.4, "Bright": 0.35, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.4, "Raspy": 0.2, "Voiceless": 0.05}');
INSERT INTO audio_file VALUES(32,'ES_Good Vibes Only.wav_11.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Good Vibes Only.wav_11.wav','{"Rock": 0.0, "Hip Hop": 0.8, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.2}','{"Emotional": 0.0, "Tense": 0.15, "Bright": 0.4, "Relaxed": 0.45}','{"Smooth": 0.2, "Dreamy": 0.0, "Raspy": 0.8, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(33,'ES_Hierarchy.wav_12.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Hierarchy.wav_12.wav','{"Rock": 1.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.6, "Bright": 0.4, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.3, "Raspy": 0.65, "Voiceless": 0.05}');
INSERT INTO audio_file VALUES(34,'ES_I Got Love.wav_13.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_I Got Love.wav_13.wav','{"Rock": 0.6, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.3}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.5, "Dreamy": 0.35, "Raspy": 0.15, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(35,'ES_Lily My Dear.wav_14.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Lily My Dear.wav_14.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 1.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.55, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(36,'ES_Our Song.wav_15.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Our Song.wav_15.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.1, "Electronic": 0.25, "Jazz": 0.0, "Korean Ballad": 0.6, "R&B/Soul": 0.05}','{"Emotional": 1.0, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 1.0, "Raspy": 0.0, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(37,'ES_Paper Crane.wav_16.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Paper Crane.wav_16.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 1.0}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.4, "Dreamy": 0.0, "Raspy": 0.6, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(38,'ES_Roundtrip.wav_17.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Roundtrip.wav_17.wav','{"Rock": 0.75, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.1, "Jazz": 0.15, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.2, "Bright": 0.8, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(39,'ES_Step on That Toe.wav_19.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Step on That Toe.wav_19.wav','{"Rock": 0.4, "Hip Hop": 0.0, "Pop Ballad": 0.1, "Electronic": 0.0, "Jazz": 0.5, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.05, "Tense": 0.1, "Bright": 0.4, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(40,'ES_There''s a Heatwave.wav_20.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_There''s a Heatwave.wav_20.wav','{"Rock": 0.0, "Hip Hop": 0.1, "Pop Ballad": 0.05, "Electronic": 0.7, "Jazz": 0.0, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.2, "Dreamy": 0.6, "Raspy": 0.05, "Voiceless": 0.15}');
INSERT INTO audio_file VALUES(41,'ES_Top Speed.wav_21.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Top Speed.wav_21.wav','{"Rock": 0.0, "Hip Hop": 0.9, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.1}','{"Emotional": 0.4, "Tense": 0.1, "Bright": 0.3, "Relaxed": 0.2}','{"Smooth": 0.3, "Dreamy": 0.4, "Raspy": 0.2, "Voiceless": 0.1}');
INSERT INTO audio_file VALUES(42,'ES_Where R U_.wav_22.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Where R U_.wav_22.wav','{"Rock": 0.0, "Hip Hop": 0.2, "Pop Ballad": 0.0, "Electronic": 0.05, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.75}','{"Emotional": 0.05, "Tense": 0.6, "Bright": 0.35, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.6, "Raspy": 0.05, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(43,'ES_Whispering Love.wav_23.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Whispering Love.wav_23.wav','{"Rock": 0.05, "Hip Hop": 0.45, "Pop Ballad": 0.0, "Electronic": 0.35, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.05}','{"Emotional": 0.0, "Tense": 0.25, "Bright": 0.7, "Relaxed": 0.05}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(44,'ES_save yourself.wav_18.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_save yourself.wav_18.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.1, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.8}','{"Emotional": 0.1, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.9}','{"Smooth": 0.05, "Dreamy": 0.8, "Raspy": 0.05, "Voiceless": 0.1}');
INSERT INTO audio_file VALUES(45,'ES_Another Life.wav_1.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Another Life.wav_1.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 1.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.35, "Relaxed": 0.6}','{"Smooth": 0.2, "Dreamy": 0.8, "Raspy": 0.0, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(46,'ES_Big Open Sky Flyer.wav_2.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Big Open Sky Flyer.wav_2.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.25, "Electronic": 0.0, "Jazz": 0.15, "Korean Ballad": 0.55, "R&B/Soul": 0.05}','{"Emotional": 0.35, "Tense": 0.0, "Bright": 0.05, "Relaxed": 0.6}','{"Smooth": 0.0, "Dreamy": 0.95, "Raspy": 0.05, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(47,'ES_Blue Texas.wav_3.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Blue Texas.wav_3.wav','{"Rock": 0.9, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.9, "Bright": 0.1, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(48,'ES_Bright Red Lights.wav_5.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Bright Red Lights.wav_5.wav','{"Rock": 0.7, "Hip Hop": 0.15, "Pop Ballad": 0.05, "Electronic": 0.1, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.3, "Tense": 0.05, "Bright": 0.65, "Relaxed": 0.0}','{"Smooth": 0.7, "Dreamy": 0.0, "Raspy": 0.15, "Voiceless": 0.15}');
INSERT INTO audio_file VALUES(49,'ES_Can''t Help It.wav_6.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Can''t Help It.wav_6.wav','{"Rock": 0.15, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.7, "Jazz": 0.05, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.95, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.45, "Raspy": 0.2, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(50,'ES_Can''t Stop.wav_7.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Can''t Stop.wav_7.wav','{"Rock": 0.15, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.7, "Jazz": 0.05, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.05, "Bright": 0.95, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.45, "Raspy": 0.2, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(51,'ES_Castle to Ruin.wav_8.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Castle to Ruin.wav_8.wav','{"Rock": 0.45, "Hip Hop": 0.0, "Pop Ballad": 0.3, "Electronic": 0.25, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.6, "Bright": 0.4, "Relaxed": 0.0}','{"Smooth": 0.15, "Dreamy": 0.45, "Raspy": 0.15, "Voiceless": 0.25}');
INSERT INTO audio_file VALUES(52,'ES_Do Over.wav_9.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Do Over.wav_9.wav','{"Rock": 0.0, "Hip Hop": 0.05, "Pop Ballad": 0.1, "Electronic": 0.4, "Jazz": 0.3, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.35, "Tense": 0.0, "Bright": 0.2, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(53,'ES_Eyes in the Back of My Head.wav_10.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Eyes in the Back of My Head.wav_10.wav','{"Rock": 0.0, "Hip Hop": 0.85, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.25, "Tense": 0.4, "Bright": 0.35, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.4, "Raspy": 0.2, "Voiceless": 0.05}');
INSERT INTO audio_file VALUES(54,'ES_Good Vibes Only.wav_11.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Good Vibes Only.wav_11.wav','{"Rock": 0.0, "Hip Hop": 0.8, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.2}','{"Emotional": 0.0, "Tense": 0.15, "Bright": 0.4, "Relaxed": 0.45}','{"Smooth": 0.2, "Dreamy": 0.0, "Raspy": 0.8, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(55,'ES_Hierarchy.wav_12.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Hierarchy.wav_12.wav','{"Rock": 1.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.6, "Bright": 0.4, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.3, "Raspy": 0.65, "Voiceless": 0.05}');
INSERT INTO audio_file VALUES(56,'ES_I Got Love.wav_13.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_I Got Love.wav_13.wav','{"Rock": 0.6, "Hip Hop": 0.1, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.3}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.5, "Dreamy": 0.35, "Raspy": 0.15, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(57,'ES_Lily My Dear.wav_14.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Lily My Dear.wav_14.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 1.0, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.55, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(58,'ES_Our Song.wav_15.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Our Song.wav_15.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.1, "Electronic": 0.25, "Jazz": 0.0, "Korean Ballad": 0.6, "R&B/Soul": 0.05}','{"Emotional": 1.0, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 1.0, "Raspy": 0.0, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(59,'ES_Paper Crane.wav_16.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Paper Crane.wav_16.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 1.0}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.4, "Dreamy": 0.0, "Raspy": 0.6, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(60,'ES_Roundtrip.wav_17.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Roundtrip.wav_17.wav','{"Rock": 0.75, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.1, "Jazz": 0.15, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.0, "Tense": 0.2, "Bright": 0.8, "Relaxed": 0.0}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(61,'ES_Step on That Toe.wav_19.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Step on That Toe.wav_19.wav','{"Rock": 0.4, "Hip Hop": 0.0, "Pop Ballad": 0.1, "Electronic": 0.0, "Jazz": 0.5, "Korean Ballad": 0.0, "R&B/Soul": 0.0}','{"Emotional": 0.05, "Tense": 0.1, "Bright": 0.4, "Relaxed": 0.45}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(62,'ES_There''s a Heatwave.wav_20.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_There''s a Heatwave.wav_20.wav','{"Rock": 0.0, "Hip Hop": 0.1, "Pop Ballad": 0.05, "Electronic": 0.7, "Jazz": 0.0, "Korean Ballad": 0.05, "R&B/Soul": 0.1}','{"Emotional": 0.0, "Tense": 0.0, "Bright": 1.0, "Relaxed": 0.0}','{"Smooth": 0.2, "Dreamy": 0.6, "Raspy": 0.05, "Voiceless": 0.15}');
INSERT INTO audio_file VALUES(63,'ES_Top Speed.wav_21.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Top Speed.wav_21.wav','{"Rock": 0.0, "Hip Hop": 0.9, "Pop Ballad": 0.0, "Electronic": 0.0, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.1}','{"Emotional": 0.4, "Tense": 0.1, "Bright": 0.3, "Relaxed": 0.2}','{"Smooth": 0.3, "Dreamy": 0.4, "Raspy": 0.2, "Voiceless": 0.1}');
INSERT INTO audio_file VALUES(64,'ES_Where R U_.wav_22.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Where R U_.wav_22.wav','{"Rock": 0.0, "Hip Hop": 0.2, "Pop Ballad": 0.0, "Electronic": 0.05, "Jazz": 0.0, "Korean Ballad": 0.0, "R&B/Soul": 0.75}','{"Emotional": 0.05, "Tense": 0.6, "Bright": 0.35, "Relaxed": 0.0}','{"Smooth": 0.35, "Dreamy": 0.6, "Raspy": 0.05, "Voiceless": 0.0}');
INSERT INTO audio_file VALUES(65,'ES_Whispering Love.wav_23.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_Whispering Love.wav_23.wav','{"Rock": 0.05, "Hip Hop": 0.45, "Pop Ballad": 0.0, "Electronic": 0.35, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.05}','{"Emotional": 0.0, "Tense": 0.25, "Bright": 0.7, "Relaxed": 0.05}','{"Smooth": 0.0, "Dreamy": 0.0, "Raspy": 0.0, "Voiceless": 1.0}');
INSERT INTO audio_file VALUES(66,'ES_save yourself.wav_18.wav','../../data_preprocessing/audio_split/audio_full_mix_split/ES_save yourself.wav_18.wav','{"Rock": 0.0, "Hip Hop": 0.0, "Pop Ballad": 0.0, "Electronic": 0.1, "Jazz": 0.1, "Korean Ballad": 0.0, "R&B/Soul": 0.8}','{"Emotional": 0.1, "Tense": 0.0, "Bright": 0.0, "Relaxed": 0.9}','{"Smooth": 0.05, "Dreamy": 0.8, "Raspy": 0.05, "Voiceless": 0.1}');
CREATE TABLE test (
	id INTEGER NOT NULL, 
	test_type INTEGER NOT NULL, 
	test_start_time DATETIME NOT NULL, 
	test_end_time DATETIME, 
	user_id INTEGER NOT NULL, 
	pre_survey_data TEXT, 
	liked_artists TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO test VALUES(1,1,'2024-04-19 12:01:50.804220','2024-04-20 06:57:05.819663',1,'{"1": ["No"], "2": [], "3": [], "4": []}','["7Ln80lUS6He07XvHI8qqHH", "2uYWxilOVlUdk4oV9DvwqK"]');
INSERT INTO test VALUES(2,1,'2024-04-20 06:57:30.535343','2024-04-20 07:03:38.255096',1,'{"1": ["No"], "2": [], "3": [], "4": []}','[]');
INSERT INTO test VALUES(3,1,'2024-04-20 07:08:46.181323','2024-04-20 07:09:55.369653',2,'{"1": ["No"], "2": [], "3": [], "4": []}','["5K4W6rqBFWDnAN6FQUkS6x"]');
INSERT INTO test VALUES(4,1,'2024-04-20 10:20:24.202641',NULL,1,'{"1": ["No"], "2": [], "3": [], "4": []}','["540vIaP2JwjQb9dm3aArA4"]');
CREATE TABLE user_answer (
	id INTEGER NOT NULL, 
	overall_rating INTEGER, 
	user_id INTEGER NOT NULL, 
	audio_id INTEGER NOT NULL, 
	test_id INTEGER NOT NULL, 
	question_index INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(audio_id) REFERENCES audio_file (id), 
	FOREIGN KEY(test_id) REFERENCES test (id)
);
INSERT INTO user_answer VALUES(1,3,1,1,1,0);
INSERT INTO user_answer VALUES(2,2,1,2,1,1);
INSERT INTO user_answer VALUES(3,2,1,3,1,2);
INSERT INTO user_answer VALUES(4,2,1,4,1,3);
INSERT INTO user_answer VALUES(5,1,1,5,1,5);
INSERT INTO user_answer VALUES(6,1,1,6,1,6);
INSERT INTO user_answer VALUES(7,1,1,7,1,7);
INSERT INTO user_answer VALUES(8,1,1,8,1,8);
INSERT INTO user_answer VALUES(9,-1,1,9,1,9);
INSERT INTO user_answer VALUES(10,-2,1,10,1,10);
INSERT INTO user_answer VALUES(11,-2,1,11,1,11);
INSERT INTO user_answer VALUES(12,-2,1,12,1,12);
INSERT INTO user_answer VALUES(13,-3,1,13,1,13);
INSERT INTO user_answer VALUES(14,2,1,14,1,14);
INSERT INTO user_answer VALUES(15,-1,1,15,1,15);
INSERT INTO user_answer VALUES(16,2,1,16,1,16);
INSERT INTO user_answer VALUES(17,-3,1,17,1,17);
INSERT INTO user_answer VALUES(18,2,1,18,1,21);
INSERT INTO user_answer VALUES(19,2,1,5,1,4);
INSERT INTO user_answer VALUES(20,1,1,6,1,5);
INSERT INTO user_answer VALUES(21,-2,1,10,1,11);
INSERT INTO user_answer VALUES(22,NULL,1,18,1,18);
INSERT INTO user_answer VALUES(23,-1,1,19,1,19);
INSERT INTO user_answer VALUES(24,1,1,20,1,20);
INSERT INTO user_answer VALUES(25,-1,1,21,1,21);
INSERT INTO user_answer VALUES(26,2,1,3,1,3);
INSERT INTO user_answer VALUES(27,-3,1,12,1,14);
INSERT INTO user_answer VALUES(28,2,1,15,1,16);
INSERT INTO user_answer VALUES(29,-3,1,17,1,18);
INSERT INTO user_answer VALUES(30,NULL,1,19,1,20);
INSERT INTO user_answer VALUES(31,NULL,1,4,1,4);
INSERT INTO user_answer VALUES(32,1,1,6,1,8);
INSERT INTO user_answer VALUES(33,1,1,6,1,9);
INSERT INTO user_answer VALUES(34,1,1,9,1,10);
INSERT INTO user_answer VALUES(35,NULL,1,11,1,13);
INSERT INTO user_answer VALUES(36,NULL,1,12,1,15);
INSERT INTO user_answer VALUES(37,3,1,14,1,17);
INSERT INTO user_answer VALUES(38,NULL,1,8,1,9);
INSERT INTO user_answer VALUES(39,NULL,1,9,1,11);
INSERT INTO user_answer VALUES(40,NULL,1,10,1,12);
INSERT INTO user_answer VALUES(41,-2,1,12,1,13);
INSERT INTO user_answer VALUES(42,-2,1,13,1,14);
INSERT INTO user_answer VALUES(43,-3,1,14,1,15);
INSERT INTO user_answer VALUES(44,NULL,1,15,1,17);
INSERT INTO user_answer VALUES(45,2,1,16,1,18);
INSERT INTO user_answer VALUES(46,2,1,18,1,20);
INSERT INTO user_answer VALUES(47,NULL,1,21,1,23);
INSERT INTO user_answer VALUES(48,NULL,1,19,1,24);
INSERT INTO user_answer VALUES(49,1,1,21,1,25);
INSERT INTO user_answer VALUES(50,1,1,22,1,28);
INSERT INTO user_answer VALUES(51,NULL,1,3,1,4);
INSERT INTO user_answer VALUES(52,2,1,4,1,5);
INSERT INTO user_answer VALUES(53,1,1,6,1,7);
INSERT INTO user_answer VALUES(54,1,1,8,1,10);
INSERT INTO user_answer VALUES(55,-1,1,9,1,12);
INSERT INTO user_answer VALUES(56,-2,1,11,1,14);
INSERT INTO user_answer VALUES(57,-2,1,11,1,16);
INSERT INTO user_answer VALUES(58,NULL,1,15,1,18);
INSERT INTO user_answer VALUES(59,-3,1,17,1,20);
INSERT INTO user_answer VALUES(60,NULL,1,19,1,22);
INSERT INTO user_answer VALUES(61,1,1,21,1,24);
INSERT INTO user_answer VALUES(62,NULL,1,20,1,27);
INSERT INTO user_answer VALUES(63,1,1,22,1,29);
INSERT INTO user_answer VALUES(64,1,1,21,1,30);
INSERT INTO user_answer VALUES(65,NULL,1,22,1,31);
INSERT INTO user_answer VALUES(66,-1,1,22,1,34);
INSERT INTO user_answer VALUES(67,NULL,1,7,1,9);
INSERT INTO user_answer VALUES(68,3,1,1,2,0);
INSERT INTO user_answer VALUES(69,-1,1,2,2,2);
INSERT INTO user_answer VALUES(70,2,1,3,2,3);
INSERT INTO user_answer VALUES(71,1,1,4,2,5);
INSERT INTO user_answer VALUES(72,-2,1,5,2,7);
INSERT INTO user_answer VALUES(73,-2,1,5,2,11);
INSERT INTO user_answer VALUES(74,1,1,6,2,12);
INSERT INTO user_answer VALUES(75,3,1,7,2,14);
INSERT INTO user_answer VALUES(76,3,1,8,2,15);
INSERT INTO user_answer VALUES(77,NULL,1,8,2,16);
INSERT INTO user_answer VALUES(78,3,1,9,2,19);
INSERT INTO user_answer VALUES(79,3,1,10,2,21);
INSERT INTO user_answer VALUES(80,-1,1,2,2,1);
INSERT INTO user_answer VALUES(81,2,1,3,2,2);
INSERT INTO user_answer VALUES(82,1,1,4,2,4);
INSERT INTO user_answer VALUES(83,-2,1,5,2,5);
INSERT INTO user_answer VALUES(84,3,1,5,2,6);
INSERT INTO user_answer VALUES(85,1,1,6,2,7);
INSERT INTO user_answer VALUES(86,1,1,6,2,8);
INSERT INTO user_answer VALUES(87,3,1,7,2,9);
INSERT INTO user_answer VALUES(88,3,1,8,2,10);
INSERT INTO user_answer VALUES(89,3,1,9,2,11);
INSERT INTO user_answer VALUES(90,NULL,1,7,2,13);
INSERT INTO user_answer VALUES(91,NULL,1,8,2,14);
INSERT INTO user_answer VALUES(92,3,1,9,2,16);
INSERT INTO user_answer VALUES(93,3,1,9,2,17);
INSERT INTO user_answer VALUES(94,3,1,10,2,18);
INSERT INTO user_answer VALUES(95,1,1,11,2,19);
INSERT INTO user_answer VALUES(96,NULL,1,10,2,20);
INSERT INTO user_answer VALUES(97,NULL,1,11,2,21);
INSERT INTO user_answer VALUES(98,NULL,1,6,2,14);
INSERT INTO user_answer VALUES(99,NULL,1,11,2,20);
INSERT INTO user_answer VALUES(100,NULL,1,11,2,22);
INSERT INTO user_answer VALUES(101,-1,1,12,2,23);
INSERT INTO user_answer VALUES(102,-1,1,13,2,24);
INSERT INTO user_answer VALUES(103,-2,1,14,2,25);
INSERT INTO user_answer VALUES(104,-2,1,15,2,26);
INSERT INTO user_answer VALUES(105,-2,1,16,2,27);
INSERT INTO user_answer VALUES(106,NULL,1,16,2,28);
INSERT INTO user_answer VALUES(107,-2,1,17,2,31);
INSERT INTO user_answer VALUES(108,-2,1,18,2,34);
INSERT INTO user_answer VALUES(109,-2,1,19,2,35);
INSERT INTO user_answer VALUES(110,NULL,1,19,2,36);
INSERT INTO user_answer VALUES(111,NULL,1,19,2,37);
INSERT INTO user_answer VALUES(112,-2,1,20,2,40);
INSERT INTO user_answer VALUES(113,NULL,1,20,2,42);
INSERT INTO user_answer VALUES(114,-2,1,21,2,43);
INSERT INTO user_answer VALUES(115,-2,1,21,2,44);
INSERT INTO user_answer VALUES(116,-2,1,22,2,48);
INSERT INTO user_answer VALUES(117,3,2,1,3,0);
INSERT INTO user_answer VALUES(118,2,2,2,3,1);
INSERT INTO user_answer VALUES(119,1,2,3,3,2);
INSERT INTO user_answer VALUES(120,3,2,4,3,3);
INSERT INTO user_answer VALUES(121,2,2,5,3,4);
INSERT INTO user_answer VALUES(122,3,2,6,3,5);
INSERT INTO user_answer VALUES(123,3,2,7,3,6);
INSERT INTO user_answer VALUES(124,2,2,8,3,7);
INSERT INTO user_answer VALUES(125,1,2,9,3,8);
INSERT INTO user_answer VALUES(126,-1,2,10,3,9);
INSERT INTO user_answer VALUES(127,3,2,11,3,10);
INSERT INTO user_answer VALUES(128,2,2,12,3,11);
INSERT INTO user_answer VALUES(129,1,2,13,3,12);
INSERT INTO user_answer VALUES(130,2,2,14,3,13);
INSERT INTO user_answer VALUES(131,3,2,15,3,14);
INSERT INTO user_answer VALUES(132,3,2,16,3,15);
INSERT INTO user_answer VALUES(133,3,2,17,3,16);
INSERT INTO user_answer VALUES(134,3,2,18,3,17);
INSERT INTO user_answer VALUES(135,3,2,19,3,18);
INSERT INTO user_answer VALUES(136,3,2,20,3,19);
INSERT INTO user_answer VALUES(137,3,2,21,3,20);
INSERT INTO user_answer VALUES(138,-2,2,22,3,21);
INSERT INTO user_answer VALUES(139,3,1,1,4,0);
INSERT INTO user_answer VALUES(140,-1,1,2,4,1);
INSERT INTO user_answer VALUES(141,3,1,3,4,2);
INSERT INTO user_answer VALUES(142,2,1,4,4,3);
INSERT INTO user_answer VALUES(143,-1,1,5,4,4);
INSERT INTO user_answer VALUES(144,-2,1,6,4,5);
INSERT INTO user_answer VALUES(145,3,1,7,4,6);
CREATE TABLE pre_survey_answer (
	id INTEGER NOT NULL, 
	question_id INTEGER NOT NULL, 
	answers TEXT NOT NULL, 
	test_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(test_id) REFERENCES test (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
COMMIT;
