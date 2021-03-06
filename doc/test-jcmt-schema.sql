CREATE TABLE FILES (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  file_id VARCHAR(70) NOT NULL,
  obsid VARCHAR(48) NOT NULL,
  subsysnr INTEGER NOT NULL,
  nsubscan INTEGER NOT NULL,
  obsid_subsysnr VARCHAR(50) NOT NULL,
  md5sum VARCHAR(40) DEFAULT NULL,
  filesize INTEGER DEFAULT NULL
);

CREATE TABLE COMMON (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  obsid VARCHAR(48) NOT NULL,
  project VARCHAR(32) DEFAULT NULL,
  survey VARCHAR(10) DEFAULT NULL,
  rmtagent VARCHAR(10) DEFAULT NULL,
  agentid VARCHAR(70) DEFAULT NULL,
  object VARCHAR(70) DEFAULT NULL,
  standard INTEGER DEFAULT NULL,
  obsnum INTEGER DEFAULT NULL,
  utdate INTEGER DEFAULT NULL,
  date_obs datetime(3) NOT NULL,
  date_end datetime(3) DEFAULT NULL,
  instap VARCHAR(8) DEFAULT NULL,
  instap_x double DEFAULT NULL,
  instap_y double DEFAULT NULL,
  amstart double DEFAULT NULL,
  amend double DEFAULT NULL,
  azstart double DEFAULT NULL,
  azend double DEFAULT NULL,
  elstart double DEFAULT NULL,
  elend double DEFAULT NULL,
  hststart datetime(3) DEFAULT NULL,
  hstend datetime(3) DEFAULT NULL,
  lststart double DEFAULT NULL,
  lstend double DEFAULT NULL,
  int_time double DEFAULT NULL,
  atstart double DEFAULT NULL,
  atend double DEFAULT NULL,
  humstart double DEFAULT NULL,
  humend double DEFAULT NULL,
  bpstart double DEFAULT NULL,
  bpend double DEFAULT NULL,
  wndspdst double DEFAULT NULL,
  wndspden double DEFAULT NULL,
  wnddirst double DEFAULT NULL,
  wnddiren double DEFAULT NULL,
  tau225st double DEFAULT NULL,
  tau225en double DEFAULT NULL,
  taudatst datetime DEFAULT NULL,
  taudaten datetime DEFAULT NULL,
  tausrc VARCHAR(16) DEFAULT NULL,
  wvmtaust double DEFAULT NULL,
  wvmtauen double DEFAULT NULL,
  wvmdatst datetime DEFAULT NULL,
  wvmdaten datetime DEFAULT NULL,
  seeingst double DEFAULT NULL,
  seeingen double DEFAULT NULL,
  seedatst datetime DEFAULT NULL,
  seedaten datetime DEFAULT NULL,
  frlegtst double DEFAULT NULL,
  frlegten double DEFAULT NULL,
  bklegtst double DEFAULT NULL,
  bklegten double DEFAULT NULL,
  sam_mode VARCHAR(8) DEFAULT NULL,
  sw_mode VARCHAR(8) DEFAULT NULL,
  obs_type VARCHAR(10) DEFAULT NULL,
  chop_crd VARCHAR(12) DEFAULT NULL,
  chop_frq double DEFAULT NULL,
  chop_pa double DEFAULT NULL,
  chop_thr double DEFAULT NULL,
  jigl_cnt INTEGER DEFAULT NULL,
  jigl_nam VARCHAR(70) DEFAULT NULL,
  jigl_pa double DEFAULT NULL,
  jigl_crd VARCHAR(12) DEFAULT NULL,
  map_hght double DEFAULT NULL,
  map_pa double DEFAULT NULL,
  map_wdth double DEFAULT NULL,
  locl_crd VARCHAR(12) DEFAULT NULL,
  map_x double DEFAULT NULL,
  map_y double DEFAULT NULL,
  scan_crd VARCHAR(12) DEFAULT NULL,
  scan_vel double DEFAULT NULL,
  scan_dy double DEFAULT NULL,
  scan_pa double DEFAULT NULL,
  scan_pat VARCHAR(28) DEFAULT NULL,
  align_dx double DEFAULT NULL,
  align_dy double DEFAULT NULL,
  focus_dz double DEFAULT NULL,
  daz double DEFAULT NULL,
  del double DEFAULT NULL,
  uaz double DEFAULT NULL,
  uel double DEFAULT NULL,
  steptime double DEFAULT NULL,
  num_cyc INTEGER DEFAULT NULL,
  jos_mult INTEGER DEFAULT NULL,
  jos_min INTEGER DEFAULT NULL,
  startidx INTEGER DEFAULT NULL,
  focaxis char(1) DEFAULT NULL,
  nfocstep INTEGER DEFAULT NULL,
  focstep double DEFAULT NULL,
  ocscfg VARCHAR(70) DEFAULT NULL,
  status VARCHAR(8) DEFAULT NULL,
  pol_conn INTEGER DEFAULT NULL,
  pol_mode VARCHAR(9) DEFAULT NULL,
  rotafreq double DEFAULT NULL,
  instrume VARCHAR(8) DEFAULT NULL,
  backend VARCHAR(8) DEFAULT NULL,
  release_date datetime DEFAULT NULL,
  obsra double DEFAULT NULL,
  obsdec double DEFAULT NULL,
  obsratl double DEFAULT NULL,
  obsrabl double DEFAULT NULL,
  obsratr double DEFAULT NULL,
  obsrabr double DEFAULT NULL,
  obsdectl double DEFAULT NULL,
  obsdecbl double DEFAULT NULL,
  obsdectr double DEFAULT NULL,
  obsdecbr double DEFAULT NULL,
  dut1 double DEFAULT NULL,
  msbtid VARCHAR(32) DEFAULT NULL,
  jig_scal double DEFAULT NULL,
  inbeam VARCHAR(64) DEFAULT NULL,
  inbeam_orig VARCHAR(64) DEFAULT NULL,
  moving_target INTEGER DEFAULT NULL,
  last_caom_mod datetime DEFAULT NULL,
  req_mintau double DEFAULT NULL,
  req_maxtau double DEFAULT NULL,
  msbtitle VARCHAR(70) DEFAULT NULL,
  oper_loc VARCHAR(70) DEFAULT NULL,
  oper_sft VARCHAR(70) DEFAULT NULL
);
