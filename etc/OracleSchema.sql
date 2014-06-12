----------------------------------------------------------------------
-- Create tables for Tier0 Data Service Database.

CREATE TABLE express_config (
  run int not null,
  stream varchar2(255) not null,
  cmssw varchar2(255) not null,
  scram_arch varchar2(50) not null,
  global_tag varchar2(50) not null,
  scenario varchar2(25) not null,
  reco_cmssw varchar2(255),
  reco_scram_arch varchar2(50),
  primary key (run, stream)
) ORGANIZATION INDEX;

CREATE TABLE reco_config (
  run int not null,
  primds varchar2(255) not null,
  cmssw varchar2(255) not null,
  scram_arch varchar2(50) not null,
  global_tag varchar2(50) not null,
  scenario varchar2(25) not null,
  primary key (run, primds)
) ORGANIZATION INDEX;

CREATE TABLE reco_locked (
  run int not null,
  locked int not null,
  primary key (run)
) ORGANIZATION INDEX;

