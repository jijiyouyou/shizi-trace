
  window.TRACE_LAYOUTS = {"word_bits":32,"bit_order":"lsb0_in_word","payloads":{"mau_mpl_req_data":{"width":373,"bit_order":"lsb0","note":"keygen_trace name=mau_mpl_req_data 拼出的向量；0..371 同 mpl 接口，372=pptrace","fields":[{"name":"lu_key_prof","bits":[3,0],"width":4,"desc":"最低位；业务 [371:0] 内"},{"name":"lu0_enable","bits":[4,4],"width":1,"desc":"图中 lu0_enbale"},{"name":"lu1_enable","bits":[5,5],"width":1,"desc":"lu1_enable"},{"name":"lu_key","bits":[325,6],"width":320,"desc":"查找 key"},{"name":"sf_read0","bits":[326,326],"width":1,"desc":"sf_read0"},{"name":"sf_read_prof0","bits":[328,327],"width":2,"desc":"sf_read_prof0"},{"name":"sf_read1","bits":[329,329],"width":1,"desc":"sf_read1"},{"name":"sf_read_prof1","bits":[331,330],"width":2,"desc":"sf_read_prof1"},{"name":"sf_read_idx0","bits":[351,332],"width":20,"desc":"sf_read_idx0"},{"name":"sf_read_idx1","bits":[371,352],"width":20,"desc":"业务最高位 [371]"},{"name":"pptrace","bits":[372,372],"width":1,"desc":"ppt / pptrace；keygen Domain 最高 1bit"}]}},"traces":{"iparser_trace":{"title":"Iparser register trace","word_count":20,"fields":[{"domain":0,"name":"dbg_hdr_info","bits":[31,0],"width":32,"desc":"hdr 相关信息"},{"domain":1,"name":"dbg_psv_info","bits":[31,0],"width":32,"desc":"psv 相关信息"},{"domain":2,"name":"dbg_ppu_out_data0_rsv","bits":[31,14],"width":18,"desc":"reserved"},{"domain":2,"name":"dbg_ppu_out_data0_pktid","bits":[13,5],"width":9,"desc":"输出的 pktid"},{"domain":2,"name":"dbg_ppu_out_data0_portid","bits":[4,0],"width":5,"desc":"输出的 portid"},{"domain":3,"name":"dbg_ppu_out_data1_hint","bits":[31,0],"width":32,"desc":"输出的 hint 信息"},{"domain":4,"name":"dbg_eof_out_data_rsv","bits":[31,28],"width":4,"desc":"reserved"},{"domain":4,"name":"dbg_eof_out_data_frm_size","bits":[27,14],"width":14,"desc":"输出的 frm_size"},{"domain":4,"name":"dbg_eof_out_data_pktid","bits":[13,5],"width":9,"desc":"输出的 pktid"},{"domain":4,"name":"dbg_eof_out_data_portid","bits":[4,0],"width":5,"desc":"输出的 portid"},{"domain":5,"name":"dbg_mpl_req_info","bits":[31,0],"width":32,"desc":"mpl 请求信息"},{"domain":6,"name":"dbg_mpl_rsp_info","bits":[31,0],"width":32,"desc":"mpl 响应信息"},{"domain":7,"name":"dbg_mpl_rsp_info1","bits":[31,0],"width":32,"desc":"mpl 响应信息 1"},{"domain":8,"name":"dbg_stg_tcam_match_rcd0","bits":[31,0],"width":32,"desc":"stg tcam match record 0"},{"domain":9,"name":"dbg_stg_tcam_match_rcd1","bits":[31,0],"width":32,"desc":"stg tcam match record 1"},{"domain":10,"name":"dbg_stg_tcam_match_rcd2","bits":[31,0],"width":32,"desc":"stg tcam match record 2"},{"domain":11,"name":"dbg_stg_info_rcd","bits":[31,0],"width":32,"desc":"stg info record"},{"domain":12,"name":"dbg_stg_done_rcd_rsv","bits":[31,4],"width":28,"desc":"reserved"},{"domain":12,"name":"dbg_stg_done_rcd_len_err","bits":[3,3],"width":1,"desc":"len error"},{"domain":12,"name":"dbg_stg_done_rcd_bad_shift","bits":[2,2],"width":1,"desc":"bad shift error"},{"domain":12,"name":"dbg_stg_done_rcd_tcam_err","bits":[1,1],"width":1,"desc":"tcam miss error"},{"domain":12,"name":"dbg_stg_done_rcd_adt_stop","bits":[0,0],"width":1,"desc":"adt stop flag"},{"domain":13,"name":"dbg_exm_info0_match_key","bits":[31,16],"width":16,"desc":"match key"},{"domain":13,"name":"dbg_exm_info0_ral_key","bits":[15,0],"width":16,"desc":"ral key"},{"domain":14,"name":"dbg_exm_info1_rsv","bits":[31,5],"width":27,"desc":"reserved"},{"domain":14,"name":"dbg_exm_info1_hit","bits":[4,4],"width":1,"desc":"match hit 标志"},{"domain":14,"name":"dbg_exm_info1_hit_idx","bits":[3,0],"width":4,"desc":"match hit idx"},{"domain":15,"name":"dbg_pstproc_check_flag","bits":[31,0],"width":32,"desc":"pst proc check flag"},{"domain":16,"name":"dbg_pstproc_dptr_rcd0_rsv","bits":[31,30],"width":2,"desc":"reserved"},{"domain":16,"name":"dbg_pstproc_dptr_rcd0_dptr4","bits":[29,24],"width":6,"desc":"dptr4"},{"domain":16,"name":"dbg_pstproc_dptr_rcd0_dptr3","bits":[23,18],"width":6,"desc":"dptr3"},{"domain":16,"name":"dbg_pstproc_dptr_rcd0_dptr2","bits":[17,12],"width":6,"desc":"dptr2"},{"domain":16,"name":"dbg_pstproc_dptr_rcd0_dptr1","bits":[11,6],"width":6,"desc":"dptr1"},{"domain":16,"name":"dbg_pstproc_dptr_rcd0_dptr0","bits":[5,0],"width":6,"desc":"dptr0"},{"domain":17,"name":"dbg_pstproc_dptr_rcd1_rsv","bits":[31,30],"width":2,"desc":"reserved"},{"domain":17,"name":"dbg_pstproc_dptr_rcd1_dptr9","bits":[29,24],"width":6,"desc":"dptr9"},{"domain":17,"name":"dbg_pstproc_dptr_rcd1_dptr8","bits":[23,18],"width":6,"desc":"dptr8"},{"domain":17,"name":"dbg_pstproc_dptr_rcd1_dptr7","bits":[17,12],"width":6,"desc":"dptr7"},{"domain":17,"name":"dbg_pstproc_dptr_rcd1_dptr6","bits":[11,6],"width":6,"desc":"dptr6"},{"domain":17,"name":"dbg_pstproc_dptr_rcd1_dptr5","bits":[5,0],"width":6,"desc":"dptr5"},{"domain":18,"name":"dbg_pstproc_dptr_rcd2_rsv","bits":[31,12],"width":20,"desc":"reserved"},{"domain":18,"name":"dbg_pstproc_dptr_rcd2_dptr11","bits":[11,6],"width":6,"desc":"dptr11"},{"domain":18,"name":"dbg_pstproc_dptr_rcd2_dptr10","bits":[5,0],"width":6,"desc":"dptr10"},{"domain":19,"name":"dbg_ctn_info_val","bits":[31,16],"width":16,"desc":"ctn_gen 的 val"},{"domain":19,"name":"dbg_ctn_info_en","bits":[15,0],"width":16,"desc":"ctn_gen 的 en"}]}},"cls_trace":{"title":"Cls trace","word_count":18,"fields":[{"domain":0,"name":"bypass_mau","bits":[0,0],"width":1,"desc":"cls 未命中或 MAU 不使能"},{"domain":0,"name":"hit_idx","bits":[4,1],"width":4,"desc":"流分类 clsd 命中索引"},{"domain":0,"name":"cls_key","bits":[20,5],"width":16,"desc":"流分类 key"},{"domain":0,"name":"rd_keg_prof1","bits":[22,21],"width":2,"desc":"Direct read1 提取 prof"},{"domain":0,"name":"rd_keg_prof0","bits":[24,23],"width":2,"desc":"Direct read0 提取 prof"},{"domain":0,"name":"lkp_keg_prof","bits":[28,25],"width":4,"desc":"Lu key gen prof"},{"domain":0,"name":"vme_keg_prof_2_0","bits":[31,29],"width":3,"desc":"Vme keygen prof[2:0]"},{"domain":1,"name":"vme_keg_prof_3","bits":[0,0],"width":1,"desc":"Vme keygen prof[3]"},{"domain":1,"name":"glb_ctl_prof","bits":[4,1],"width":4,"desc":"Global ctrl prof"},{"domain":1,"name":"igr_port","bits":[9,5],"width":5,"desc":"入口 port（图中 igr_porf）"},{"domain":1,"name":"rsv","bits":[31,10],"width":22,"desc":"保留"},{"domain":2,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[31:0]"},{"domain":3,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[63:32]"},{"domain":4,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[95:64]"},{"domain":5,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[127:96]"},{"domain":6,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[159:128]"},{"domain":7,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[191:160]"},{"domain":8,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[223:192]"},{"domain":9,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[255:224]"},{"domain":10,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[287:256]"},{"domain":11,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[319:288]"},{"domain":12,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[351:320]"},{"domain":13,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[383:352]"},{"domain":14,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[415:384]"},{"domain":15,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[447:416]"},{"domain":16,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[479:448]"},{"domain":17,"name":"igr_psv","bits":[31,0],"width":32,"desc":"igr_psv[511:480]"}]},"keygen_trace":{"title":"keygen trace","word_count":29,"fields":[{"domain":0,"name":"mpl_req","bits":[0,0],"width":1,"desc":"mau 查询 mpl 有效指示"},{"domain":0,"name":"lpm_req","bits":[1,1],"width":1,"desc":"mau 查询 lpm 有效指示"},{"domain":0,"name":"mau_mpl_req_data","bits":[31,2],"width":30,"desc":"拼入 payloads.mau_mpl_req_data[29:0]"},{"domain":1,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [61:30]"},{"domain":2,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [93:62]"},{"domain":3,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [125:94]"},{"domain":4,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [157:126]"},{"domain":5,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [189:158]"},{"domain":6,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [221:190]"},{"domain":7,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [253:222]"},{"domain":8,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [285:254]"},{"domain":9,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [317:286]"},{"domain":10,"name":"mau_mpl_req_data","bits":[31,0],"width":32,"desc":"拼入 [349:318]"},{"domain":11,"name":"rsv","bits":[31,24],"width":8,"desc":"保留"},{"domain":11,"name":"pass_through_psv","bits":[23,23],"width":1,"desc":"透传 psv 指示"},{"domain":11,"name":"mau_mpl_req_data","bits":[22,0],"width":23,"desc":"拼入 [372:350]；其中 [372]=pptrace"},{"domain":12,"name":"mau_lpm_req_data","bits":[31,0],"width":32,"desc":"lpm[31:0]"},{"domain":13,"name":"mau_lpm_req_data","bits":[31,0],"width":32,"desc":"lpm[63:32]"},{"domain":14,"name":"mau_lpm_req_data","bits":[31,0],"width":32,"desc":"lpm[95:64]"},{"domain":15,"name":"mau_lpm_req_data","bits":[31,0],"width":32,"desc":"lpm[127:96]"},{"domain":16,"name":"mau_lpm_req_data","bits":[31,0],"width":32,"desc":"lpm[159:128]"},{"domain":17,"name":"mau_lpm_req_data","bits":[31,0],"width":32,"desc":"lpm[191:160]"},{"domain":18,"name":"mau_lpm_req_data","bits":[31,0],"width":32,"desc":"lpm[223:192]"},{"domain":19,"name":"mau_lpm_req_data","bits":[31,0],"width":32,"desc":"lpm[255:224]"},{"domain":20,"name":"mau_lpm_req_data","bits":[17,0],"width":18,"desc":"lpm[272:256]（图宽 18）"},{"domain":20,"name":"pass_through_psv","bits":[18,18],"width":1,"desc":"透传 PSV 指示"},{"domain":20,"name":"rsv","bits":[31,19],"width":14,"desc":"保留"},{"domain":21,"name":"paw","bits":[31,0],"width":32,"desc":"paw[31:0]"},{"domain":22,"name":"paw","bits":[31,0],"width":32,"desc":"paw[63:32]"},{"domain":23,"name":"paw","bits":[31,0],"width":32,"desc":"paw[95:64]"},{"domain":24,"name":"paw","bits":[31,0],"width":32,"desc":"paw[127:96]"},{"domain":25,"name":"paw","bits":[31,0],"width":32,"desc":"paw[159:128]"},{"domain":26,"name":"paw","bits":[31,0],"width":32,"desc":"paw[191:160]"},{"domain":27,"name":"paw","bits":[31,0],"width":32,"desc":"paw[223:192]"},{"domain":28,"name":"paw","bits":[31,0],"width":32,"desc":"paw[255:224]"}]},"vme_lama_trace":{"title":"VME0 lama trace","word_count":26,"domain_base":0,"fields":[{"domain":0,"name":"aval","bits":[31,0],"width":32,"desc":"i_aval"},{"domain":1,"name":"bval","bits":[31,0],"width":32,"desc":"i_bval"},{"domain":2,"name":"mux_sel","bits":[7,0],"width":8,"desc":"{mux_sel[0..3]}"},{"domain":2,"name":"lam_idx","bits":[10,8],"width":3,"desc":"Lam_idx"},{"domain":2,"name":"rsv","bits":[11,11],"width":1,"desc":"Rsv"},{"domain":2,"name":"luta_idx","bits":[13,12],"width":2,"desc":"Luta_idx"},{"domain":2,"name":"Lut_rlt","bits":[14,14],"width":1,"desc":"1bit Lut 查找结果"},{"domain":2,"name":"rsv","bits":[15,15],"width":1,"desc":"Rsv"},{"domain":2,"name":"alu_opcode3","bits":[23,16],"width":8,"desc":"alu_opcode3"},{"domain":2,"name":"alu_opcode2","bits":[31,24],"width":8,"desc":"alu_opcode2"},{"domain":3,"name":"alu_opcode1","bits":[7,0],"width":8,"desc":"alu_opcode1"},{"domain":3,"name":"alu_opcode0","bits":[15,8],"width":8,"desc":"alu_opcode0"},{"domain":3,"name":"yval_vld","bits":[19,16],"width":4,"desc":"{vld[0..3]}"},{"domain":3,"name":"yval3","bits":[27,20],"width":8,"desc":"yval[3]"},{"domain":3,"name":"yval2_lo","bits":[31,28],"width":4,"desc":"yval[2][3:0]"},{"domain":4,"name":"yval2_hi","bits":[3,0],"width":4,"desc":"yval[2][7:4]"},{"domain":4,"name":"yval1","bits":[11,4],"width":8,"desc":"yval[1]"},{"domain":4,"name":"yval0","bits":[19,12],"width":8,"desc":"yval[0]"},{"domain":4,"name":"yval_btot3","bits":[27,20],"width":8,"desc":"yval_btot[3]（图宽标 4，按 [27:20] 为 8）"},{"domain":4,"name":"yval_btot2","bits":[31,28],"width":4,"desc":"yval_btot[2]"},{"domain":5,"name":"yval_btot1","bits":[3,0],"width":4,"desc":"yval_btot[1]"},{"domain":5,"name":"yval_btot0","bits":[7,4],"width":4,"desc":"yval_btot[0]"},{"domain":5,"name":"rsv","bits":[31,8],"width":24,"desc":"Rsv"},{"domain":6,"name":"Paw0","bits":[31,0],"width":32,"desc":"Paw0[31:0]"},{"domain":7,"name":"Paw0","bits":[31,0],"width":32,"desc":"Paw0[63:32]"},{"domain":8,"name":"Paw0","bits":[31,0],"width":32,"desc":"Paw0[95:64]"},{"domain":9,"name":"Paw0","bits":[31,0],"width":32,"desc":"Paw0[127:96]"},{"domain":10,"name":"Paw1","bits":[31,0],"width":32,"desc":"Paw1[31:0]"},{"domain":11,"name":"Paw1","bits":[31,0],"width":32,"desc":"Paw1[63:32]"},{"domain":12,"name":"Paw1","bits":[31,0],"width":32,"desc":"Paw1[95:64]"},{"domain":13,"name":"Paw1","bits":[31,0],"width":32,"desc":"Paw1[127:96]"},{"domain":14,"name":"Paw2","bits":[31,0],"width":32,"desc":"Paw2[31:0]"},{"domain":15,"name":"Paw2","bits":[31,0],"width":32,"desc":"Paw2[63:32]"},{"domain":16,"name":"Paw2","bits":[31,0],"width":32,"desc":"Paw2[95:64]"},{"domain":17,"name":"Paw2","bits":[31,0],"width":32,"desc":"Paw2[127:96]"},{"domain":18,"name":"Paw3","bits":[31,0],"width":32,"desc":"Paw3[31:0]"},{"domain":19,"name":"Paw3","bits":[31,0],"width":32,"desc":"Paw3[63:32]"},{"domain":20,"name":"Paw3","bits":[31,0],"width":32,"desc":"Paw3[95:64]"},{"domain":21,"name":"Paw3","bits":[31,0],"width":32,"desc":"Paw3[127:96]"},{"domain":22,"name":"Paw4","bits":[31,0],"width":32,"desc":"Paw4[31:0]"},{"domain":23,"name":"Paw4","bits":[31,0],"width":32,"desc":"Paw4[63:32]"},{"domain":24,"name":"Paw4","bits":[31,0],"width":32,"desc":"Paw4[95:64]"},{"domain":25,"name":"Paw4","bits":[31,0],"width":32,"desc":"Paw4[127:96]"}]},"vme_lamb_trace":{"title":"VME0 lamb trace","word_count":26,"domain_base":26,"note":"VME1~VME4 数据结构同 lama+lamb；绝对 Domain = 26 + lama 相对序号","fields":[{"domain":26,"name":"aval","bits":[31,0],"width":32,"desc":"i_aval"},{"domain":27,"name":"bval","bits":[31,0],"width":32,"desc":"i_bval"},{"domain":28,"name":"mux_sel","bits":[7,0],"width":8,"desc":"{mux_sel[0..3]}"},{"domain":28,"name":"lam_idx","bits":[10,8],"width":3,"desc":"Lam_idx"},{"domain":28,"name":"rsv","bits":[11,11],"width":1,"desc":"Rsv"},{"domain":28,"name":"luta_idx","bits":[13,12],"width":2,"desc":"Luta_idx"},{"domain":28,"name":"Lut_rlt","bits":[14,14],"width":1,"desc":"1bit Lut 查找结果"},{"domain":28,"name":"rsv","bits":[15,15],"width":1,"desc":"Rsv"},{"domain":28,"name":"alu_opcode3","bits":[23,16],"width":8,"desc":"alu_opcode3"},{"domain":28,"name":"alu_opcode2","bits":[31,24],"width":8,"desc":"alu_opcode2"},{"domain":29,"name":"alu_opcode1","bits":[7,0],"width":8,"desc":"alu_opcode1"},{"domain":29,"name":"alu_opcode0","bits":[15,8],"width":8,"desc":"alu_opcode0"},{"domain":29,"name":"yval_vld","bits":[19,16],"width":4,"desc":"{vld[0..3]}"},{"domain":29,"name":"yval3","bits":[27,20],"width":8,"desc":"yval[3]"},{"domain":29,"name":"yval2_lo","bits":[31,28],"width":4,"desc":"yval[2][3:0]"},{"domain":30,"name":"yval2_hi","bits":[3,0],"width":4,"desc":"yval[2][7:4]"},{"domain":30,"name":"yval1","bits":[11,4],"width":8,"desc":"yval[1]"},{"domain":30,"name":"yval0","bits":[19,12],"width":8,"desc":"yval[0]"},{"domain":30,"name":"yval_btot3","bits":[27,20],"width":8,"desc":"yval_btot[3]"},{"domain":30,"name":"yval_btot2","bits":[31,28],"width":4,"desc":"yval_btot[2]"},{"domain":31,"name":"yval_btot1","bits":[3,0],"width":4,"desc":"yval_btot[1]"},{"domain":31,"name":"yval_btot0","bits":[7,4],"width":4,"desc":"yval_btot[0]"},{"domain":31,"name":"rsv","bits":[31,8],"width":24,"desc":"Rsv"},{"domain":32,"name":"Paw0","bits":[31,0],"width":32,"desc":"Paw0[31:0]"},{"domain":33,"name":"Paw0","bits":[31,0],"width":32,"desc":"Paw0[63:32]"},{"domain":34,"name":"Paw0","bits":[31,0],"width":32,"desc":"Paw0[95:64]"},{"domain":35,"name":"Paw0","bits":[31,0],"width":32,"desc":"Paw0[127:96]"},{"domain":36,"name":"Paw1","bits":[31,0],"width":32,"desc":"Paw1[31:0]"},{"domain":37,"name":"Paw1","bits":[31,0],"width":32,"desc":"Paw1[63:32]"},{"domain":38,"name":"Paw1","bits":[31,0],"width":32,"desc":"Paw1[95:64]"},{"domain":39,"name":"Paw1","bits":[31,0],"width":32,"desc":"Paw1[127:96]"},{"domain":40,"name":"Paw2","bits":[31,0],"width":32,"desc":"Paw2[31:0]"},{"domain":41,"name":"Paw2","bits":[31,0],"width":32,"desc":"Paw2[63:32]"},{"domain":42,"name":"Paw2","bits":[31,0],"width":32,"desc":"Paw2[95:64]"},{"domain":43,"name":"Paw2","bits":[31,0],"width":32,"desc":"Paw2[127:96]"},{"domain":44,"name":"Paw3","bits":[31,0],"width":32,"desc":"Paw3[31:0]"},{"domain":45,"name":"Paw3","bits":[31,0],"width":32,"desc":"Paw3[63:32]"},{"domain":46,"name":"Paw3","bits":[31,0],"width":32,"desc":"Paw3[95:64]"},{"domain":47,"name":"Paw3","bits":[31,0],"width":32,"desc":"Paw3[127:96]"},{"domain":48,"name":"Paw4","bits":[31,0],"width":32,"desc":"Paw4[31:0]"},{"domain":49,"name":"Paw4","bits":[31,0],"width":32,"desc":"Paw4[63:32]"},{"domain":50,"name":"Paw4","bits":[31,0],"width":32,"desc":"Paw4[95:64]"},{"domain":51,"name":"Paw4","bits":[31,0],"width":32,"desc":"Paw4[127:96]"}]},"lrr_trace":{"title":"llr/lrr trace","word_count":26,"fields":[{"domain":0,"name":"ctn_u16_en","bits":[15,0],"width":16,"desc":"ctn_u16_en[0]"},{"domain":0,"name":"ctn_u16_en","bits":[31,16],"width":16,"desc":"ctn_u16_en[1]"},{"domain":1,"name":"ctn_u16_en","bits":[15,0],"width":16,"desc":"ctn_u16_en[2]"},{"domain":1,"name":"ctn_u16_en","bits":[31,16],"width":16,"desc":"ctn_u16_en[3]"},{"domain":2,"name":"ctn_u16_en","bits":[15,0],"width":16,"desc":"ctn_u16_en[4]"},{"domain":2,"name":"ctn_u16_en","bits":[31,16],"width":16,"desc":"ctn_u16_en[5]"},{"domain":3,"name":"ctn_u16_en","bits":[15,0],"width":16,"desc":"ctn_u16_en[6]"},{"domain":3,"name":"ctn_u16_en","bits":[31,16],"width":16,"desc":"ctn_u16_en[7]"},{"domain":4,"name":"ctn_u16_en","bits":[15,0],"width":16,"desc":"ctn_u16_en[8]"},{"domain":4,"name":"ctn_u16_en","bits":[31,16],"width":16,"desc":"ctn_u16_en[9]"},{"domain":5,"name":"ctn_u16_en","bits":[15,0],"width":16,"desc":"ctn_u16_en[10]"},{"domain":5,"name":"ctn_u16_en","bits":[31,16],"width":16,"desc":"ctn_u16_en[11]"},{"domain":6,"name":"ctn_u16_en","bits":[15,0],"width":16,"desc":"ctn_u16_en[12]"},{"domain":6,"name":"ctn_u16_en","bits":[31,16],"width":16,"desc":"ctn_u16_en[13]"},{"domain":7,"name":"ctn_u16_en","bits":[15,0],"width":16,"desc":"ctn_u16_en[14]"},{"domain":7,"name":"ctn_u16_en","bits":[31,16],"width":16,"desc":"ctn_u16_en[15]"},{"domain":8,"name":"ctn_u16_val","bits":[15,0],"width":16,"desc":"ctn_u16_val[0]"},{"domain":8,"name":"ctn_u16_val","bits":[31,16],"width":16,"desc":"ctn_u16_val[1]"},{"domain":9,"name":"ctn_u16_val","bits":[15,0],"width":16,"desc":"ctn_u16_val[2]"},{"domain":9,"name":"ctn_u16_val","bits":[31,16],"width":16,"desc":"ctn_u16_val[3]"},{"domain":10,"name":"ctn_u16_val","bits":[15,0],"width":16,"desc":"ctn_u16_val[4]"},{"domain":10,"name":"ctn_u16_val","bits":[31,16],"width":16,"desc":"ctn_u16_val[5]"},{"domain":11,"name":"ctn_u16_val","bits":[15,0],"width":16,"desc":"ctn_u16_val[6]"},{"domain":11,"name":"ctn_u16_val","bits":[31,16],"width":16,"desc":"ctn_u16_val[7]"},{"domain":12,"name":"ctn_u16_val","bits":[15,0],"width":16,"desc":"ctn_u16_val[8]"},{"domain":12,"name":"ctn_u16_val","bits":[31,16],"width":16,"desc":"ctn_u16_val[9]"},{"domain":13,"name":"ctn_u16_val","bits":[15,0],"width":16,"desc":"ctn_u16_val[10]"},{"domain":13,"name":"ctn_u16_val","bits":[31,16],"width":16,"desc":"ctn_u16_val[11]"},{"domain":14,"name":"ctn_u16_val","bits":[15,0],"width":16,"desc":"ctn_u16_val[12]"},{"domain":14,"name":"ctn_u16_val","bits":[31,16],"width":16,"desc":"ctn_u16_val[13]"},{"domain":15,"name":"ctn_u16_val","bits":[15,0],"width":16,"desc":"ctn_u16_val[14]"},{"domain":15,"name":"ctn_u16_val","bits":[31,16],"width":16,"desc":"ctn_u16_val[15]"},{"domain":16,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[31:0]"},{"domain":17,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[63:32]"},{"domain":18,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[95:64]"},{"domain":19,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[127:96]"},{"domain":20,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[159:128]"},{"domain":21,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[191:160]"},{"domain":22,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[223:192]"},{"domain":23,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[255:224]"},{"domain":24,"name":"Lur","bits":[31,0],"width":32,"desc":"Lur[287:256]"},{"domain":25,"name":"Lur","bits":[9,0],"width":10,"desc":"Lur[297:288]"},{"domain":25,"name":"rsv","bits":[31,10],"width":22,"desc":"保留"}]},"egr_trace":{"title":"egr trace","word_count":54,"fields":[{"domain":0,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[31:0]"},{"domain":1,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[63:32]"},{"domain":2,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[95:64]"},{"domain":3,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[127:96]"},{"domain":4,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[159:128]"},{"domain":5,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[191:160]"},{"domain":6,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[223:192]"},{"domain":7,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[255:224]"},{"domain":8,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[287:256]"},{"domain":9,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[319:288]"},{"domain":10,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[351:320]"},{"domain":11,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[383:352]"},{"domain":12,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[415:384]"},{"domain":13,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[447:416]"},{"domain":14,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[479:448]"},{"domain":15,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs0 提取 psv[511:480]"},{"domain":16,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[31:0]"},{"domain":17,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[63:32]"},{"domain":18,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[95:64]"},{"domain":19,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[127:96]"},{"domain":20,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[159:128]"},{"domain":21,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[191:160]"},{"domain":22,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[223:192]"},{"domain":23,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[255:224]"},{"domain":24,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[287:256]"},{"domain":25,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[319:288]"},{"domain":26,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[351:320]"},{"domain":27,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[383:352]"},{"domain":28,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[415:384]"},{"domain":29,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[447:416]"},{"domain":30,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[479:448]"},{"domain":31,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs1 提取 psv[511:480]（图中误写 [511:32]）"},{"domain":32,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[31:0]"},{"domain":33,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[63:32]"},{"domain":34,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[95:64]"},{"domain":35,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[127:96]"},{"domain":36,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[159:128]"},{"domain":37,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[191:160]"},{"domain":38,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[223:192]"},{"domain":39,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[255:224]"},{"domain":40,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[287:256]"},{"domain":41,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[319:288]"},{"domain":42,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[351:320]"},{"domain":43,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[383:352]"},{"domain":44,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[415:384]"},{"domain":45,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[447:416]"},{"domain":46,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[479:448]"},{"domain":47,"name":"egr_psv","bits":[31,0],"width":32,"desc":"ofs2 提取 psv[511:480]（图中误写 [511:32]）"},{"domain":48,"name":"lpm_result","bits":[31,0],"width":32,"desc":"lpm[31:0]"},{"domain":49,"name":"lpm_result","bits":[31,0],"width":32,"desc":"lpm[63:32]"},{"domain":50,"name":"lpm_result","bits":[11,0],"width":12,"desc":"lpm[75:64]"},{"domain":50,"name":"rsv","bits":[31,12],"width":20,"desc":"rsv"},{"domain":51,"name":"local_engine_result","bits":[31,0],"width":32,"desc":"Local engine rsp data[31:0]"},{"domain":52,"name":"local_engine_result","bits":[31,0],"width":32,"desc":"Local engine rsp data[63:32]"},{"domain":53,"name":"local_engine_result","bits":[31,0],"width":32,"desc":"Local engine rsp data[95:64]"}]}}};
  window.TRACE_RESULT = null;
  </script>
  <script>
(function () {
  "use strict";

  const L = window.TRACE_LAYOUTS;
  if (!L || !L.traces) {
    document.getElementById("statusBar").textContent = "错误：未嵌入格式表，请运行 build_viewer.py";
    return;
  }

  const IPP = [0,1,2,3,4,5,6,7,8];
  const EPP = [9,10];
  const TRACE_ORDER = ["cls","keygen","vme0","vme1","vme2","vme3","vme4","lrr","egr"];
  const PAW_NAME_RE = /^Paw\d+$/i;

  let state = {
    module: "mau",
    result: null,
    selection: null, // { type, mau, seg, mplIndex }
    lastFields: [],
  };

  /* ---------- hex / bit helpers ---------- */
  function parseU32Tokens(text) {
    if (!text || !String(text).trim()) throw new Error("空输入");
    const re = /0x[0-9a-fA-F]+|\b[0-9a-fA-F]{8}\b|\b\d+\b/g;
    const tokens = String(text).match(re);
    if (!tokens) throw new Error("未找到合法 hex/数值");
    return tokens.map((t) => {
      let v;
      if (/^0x/i.test(t)) v = parseInt(t, 16);
      else if (/^[0-9a-fA-F]{8}$/.test(t)) v = parseInt(t, 16);
      else v = parseInt(t, 10);
      if (!Number.isFinite(v) || v < 0 || v > 0xffffffff) throw new Error("非法/超出 u32: " + t);
      return v >>> 0;
    });
  }

  function extractBits(word, hi, lo) {
    if (hi < lo || lo < 0 || hi > 31) throw new Error("非法 bits [" + hi + ":" + lo + "]");
    const width = hi - lo + 1;
    const mask = width === 32 ? 0xffffffff : ((1 << width) - 1) >>> 0;
    return ((word >>> lo) & mask) >>> 0;
  }

  function fmtVal(val, width) {
    const hexW = Math.max(1, Math.ceil(width / 4));
    let hex;
    if (typeof val === "bigint") hex = "0x" + val.toString(16);
    else hex = "0x" + (val >>> 0).toString(16).padStart(hexW, "0");
    const dec = val.toString();
    let bin = "";
    if (typeof val !== "bigint" && width <= 64) bin = "0b" + (val >>> 0).toString(2).padStart(width, "0");
    else bin = "0b…(" + width + "bit)";
    return { hex, dec, bin };
  }

  function fieldRow(domain, name, hi, lo, width, value, desc) {
    const f = fmtVal(value, width);
    const reserved = /^(rsv|reserved)$/i.test(name) || (desc && desc.indexOf("保留") >= 0);
    return {
      domain, name, bits: "[" + hi + ":" + lo + "]", hi, lo, width,
      value, value_hex: f.hex, value_dec: f.dec, value_bin: f.bin,
      desc: desc || "", reserved,
    };
  }

  function decodeTrace(words, layout, allowShort) {
    const need = layout.word_count | 0;
    const domainBase = (layout.domain_base | 0) || 0;
    const minLen = need && domainBase ? domainBase + need : need;
    if (minLen && words.length < minLen && !allowShort) {
      throw new Error("长度不足：需要 " + minLen + " 个 Domain，实际 " + words.length);
    }
    const w = (need && !domainBase && words.length > need) ? words.slice(0, need) : words.slice();
    const rows = [];
    const errors = [];
    (layout.fields || []).forEach((fd) => {
      const domain = fd.domain | 0;
      const hi = fd.bits[0] | 0, lo = fd.bits[1] | 0;
      const width = fd.width != null ? fd.width | 0 : hi - lo + 1;
      if (domain < 0 || domain >= w.length) {
        errors.push("D" + domain + " 越界: " + fd.name);
        return;
      }
      try {
        const val = extractBits(w[domain], hi, lo);
        rows.push(fieldRow(domain, fd.name, hi, lo, width, val, fd.desc));
      } catch (e) {
        errors.push("D" + domain + " " + fd.name + ": " + e.message);
      }
    });
    return {
      title: layout.title || "",
      word_count: need,
      words: w.map((x) => "0x" + (x >>> 0).toString(16).padStart(8, "0")),
      fields: rows,
      errors,
    };
  }

  function assemblePayloadBits(words, fieldName, layout) {
    let acc = 0n;
    let bitPos = 0n;
    (layout.fields || []).forEach((fd) => {
      if (fd.name !== fieldName) return;
      const domain = fd.domain | 0;
      const hi = fd.bits[0] | 0, lo = fd.bits[1] | 0;
      const width = fd.width != null ? fd.width | 0 : hi - lo + 1;
      if (domain >= words.length) throw new Error("拼包缺 Domain D" + domain);
      const piece = BigInt(extractBits(words[domain], hi, lo));
      acc |= piece << bitPos;
      bitPos += BigInt(width);
    });
    return acc;
  }

  function decodePayload(bitvec, payloadLayout) {
    const rows = [];
    (payloadLayout.fields || []).forEach((fd) => {
      const hi = fd.bits[0] | 0, lo = fd.bits[1] | 0;
      const width = fd.width != null ? fd.width | 0 : hi - lo + 1;
      const mask = (1n << BigInt(width)) - 1n;
      const val = (bitvec >> BigInt(lo)) & mask;
      const num = width <= 53 ? Number(val) : val;
      rows.push(fieldRow(null, fd.name, hi, lo, width, num, fd.desc));
    });
    return {
      title: "mau_mpl_req_data",
      width: payloadLayout.width | 0,
      bitvec_hex: "0x" + bitvec.toString(16),
      fields: rows,
      note: payloadLayout.note || "",
    };
  }

  function decodeMpl(words) {
    if (!words.length) throw new Error("mpl：空输入");
    let bitvec = 0n;
    words.forEach((w, i) => { bitvec |= BigInt(w >>> 0) << BigInt(32 * i); });
    return decodePayload(bitvec, L.payloads.mau_mpl_req_data);
  }

  function groupPawRows(fields) {
    const other = [];
    const pawRows = [];
    let i = 0;
    while (i < fields.length) {
      const f = fields[i];
      const name = String(f.name || "");
      if (!PAW_NAME_RE.test(name)) { other.push(f); i++; continue; }
      const group = [f];
      let j = i + 1;
      while (j < fields.length && String(fields[j].name || "") === name) { group.push(fields[j]); j++; }
      for (let k = 0; k < group.length; k += 4) {
        const chunk = group.slice(k, k + 4);
        const rev = chunk.slice().reverse();
        pawRows.push({
          name,
          words_hex: rev.map((c) => c.value_hex),
          domains: rev.map((c) => c.domain),
          width_bits: 32 * chunk.length,
        });
      }
      i = j;
    }
    return { other, pawRows };
  }

  function attachPawView(decoded) {
    if (!decoded || !decoded.fields) return decoded;
    const { other, pawRows } = groupPawRows(decoded.fields);
    if (!pawRows.length) return decoded;
    return Object.assign({}, decoded, { fields: other, paw_rows: pawRows });
  }

  function decodeVme(words, vmeIndex) {
    const need = 52;
    if (words.length < need) throw new Error("vme 长度不足：需要 " + need + "，实际 " + words.length);
    const w = words.slice(0, need);
    return {
      title: vmeIndex != null ? ("VME" + vmeIndex + " trace") : "VME trace",
      word_count: need,
      words: w.map((x) => "0x" + (x >>> 0).toString(16).padStart(8, "0")),
      lama: attachPawView(decodeTrace(w, L.traces.vme_lama_trace)),
      lamb: attachPawView(decodeTrace(w, L.traces.vme_lamb_trace)),
      errors: [],
    };
  }

  function previewMplReqFromKeygen(words) {
    const keygen = L.traces.keygen_trace;
    const need = keygen.word_count | 0;
    if (words.length < need) throw new Error("keygen 长度不足：需要 " + need + "，实际 " + words.length);
    const bitvec = assemblePayloadBits(words.slice(0, need), "mau_mpl_req_data", keygen);
    return decodePayload(bitvec, L.payloads.mau_mpl_req_data);
  }

  function decodeIparser(words) {
    if (!L.traces.iparser_trace) throw new Error("iparser: 格式表未定义");
    return decodeTrace(words, L.traces.iparser_trace);
  }

  function decodeSegment(seg, words) {
    const s = String(seg).toLowerCase().replace(/_trace$/, "");
    const vm = /^vme(\d)$/.exec(s);
    if (s === "vme" || vm) return decodeVme(words, vm ? +vm[1] : null);
    if (s === "iparser") return decodeIparser(words);
    const map = {
      cls: "cls_trace",
      keygen: "keygen_trace",
      lrr: "lrr_trace",
      llr: "lrr_trace",
      egr: "egr_trace",
    };
    const key = map[s];
    if (!key || !L.traces[key]) throw new Error("未知子段: " + seg);
    const out = decodeTrace(words, L.traces[key]);
    if (s === "keygen") {
      try {
        out.mau_mpl_req_data = previewMplReqFromKeygen(words);
      } catch (e) {
        out.errors = (out.errors || []).concat(["mau_mpl_req_data: " + e.message]);
      }
    }
    return out;
  }

  function mauDirection(i) {
    if (IPP.indexOf(i) >= 0) return "ipp";
    if (EPP.indexOf(i) >= 0) return "epp";
    throw new Error("mau 索引越界: " + i);
  }

  /* ---------- log parse ---------- */
  const BLOCK_RE = /----\s*([\w.]+)\s+(start|end)\s*----/gi;

  function extractBlocks(text) {
    const matches = [];
    let m;
    const re = new RegExp(BLOCK_RE.source, "gi");
    while ((m = re.exec(text))) {
      matches.push({ name: m[1], kind: m[2].toLowerCase(), index: m.index, end: re.lastIndex });
    }
    if (!matches.length) {
      return [{ name: "raw", text, kind: "raw", start: 0, end: text.length }];
    }
    const stack = [];
    const blocks = [];
    matches.forEach((mk) => {
      if (mk.kind === "start") stack.push({ name: mk.name, contentStart: mk.end });
      else {
        for (let i = stack.length - 1; i >= 0; i--) {
          if (stack[i].name.toLowerCase() === mk.name.toLowerCase()) {
            const s = stack.splice(i, 1)[0];
            blocks.push({
              name: s.name,
              text: text.slice(s.contentStart, mk.index),
              kind: "block",
              start: s.contentStart,
              end: mk.index,
            });
            break;
          }
        }
      }
    });
    return blocks;
  }

  function normalizeSeg(name) {
    let n = name.trim().toLowerCase();
    if (n.endsWith("_trace")) n = n.slice(0, -6);
    if (n === "llr") return "lrr";
    if (["cls", "keygen", "egr", "lrr"].indexOf(n) >= 0) return n;
    const vm = /^vme(\d)$/.exec(n);
    if (vm) return "vme" + vm[1];
    return n;
  }

  function parseLog(text) {
    const blocks = extractBlocks(text);
    const errors = [];
    const mauSpans = [];
    const iparserRaw = [];
    blocks.forEach((b) => {
      const mm = /^mau(\d+)$/i.exec(b.name);
      if (mm && b.kind === "block") mauSpans.push({ mau: +mm[1], start: b.start, end: b.end });
      if (/^iparser(?:_trace)?$/i.test(b.name) && b.kind === "block") {
        try { iparserRaw.push({ label: b.name, words: parseU32Tokens(b.text) }); }
        catch (e) { errors.push("iparser: " + e.message); }
      }
    });

    const mauData = {};
    mauSpans.forEach((s) => { mauData[s.mau] = { trace: {}, statistics: {} }; });
    const orphans = [];

    function owningMau(pos) {
      for (let i = 0; i < mauSpans.length; i++) {
        const s = mauSpans[i];
        if (pos >= s.start && pos < s.end) return s.mau;
      }
      return null;
    }

    const mplRaw = [];

    blocks.forEach((b) => {
      if (/^mau\d+$/i.test(b.name)) return;
      if (/^mpl(?:_trace|_req|_dump)?$/i.test(b.name)) {
        try { mplRaw.push({ label: b.name, words: parseU32Tokens(b.text) }); }
        catch (e) { errors.push("mpl: " + e.message); }
        return;
      }
      const seg = normalizeSeg(b.name);
      if (seg === "raw") {
        try { orphans.push({ name: "raw", words: parseU32Tokens(b.text) }); }
        catch (e) { errors.push(e.message); }
        return;
      }
      const isStat = /^stat/i.test(seg) || /statistics/i.test(b.name);
      if (["cls","keygen","lrr","egr"].indexOf(seg) >= 0 || /^vme\d$/.test(seg) || isStat) {
        let words = [];
        try {
          if (String(b.text || "").trim()) words = parseU32Tokens(b.text);
        } catch (e) {
          if (!isStat) { errors.push(b.name + ": " + e.message); return; }
        }
        const owner = owningMau(b.start || 0);
        const meta = {
          label: b.name, words, word_count: words.length,
          category: isStat ? "statistics" : "trace",
        };
        const bucket = isStat ? "statistics" : "trace";
        const keyName = isStat ? "statistics" : seg;
        if (owner == null) orphans.push({ name: keyName, ...meta });
        else {
          if (!mauData[owner]) mauData[owner] = { trace: {}, statistics: {} };
          if (!mauData[owner].trace) mauData[owner] = { trace: mauData[owner].segments || {}, statistics: {} };
          mauData[owner][bucket][keyName] = meta;
        }
      }
    });

    if (!Object.keys(mauData).length && !orphans.length && !mplRaw.length) {
      try { orphans.push({ name: "raw", words: parseU32Tokens(text) }); }
      catch (e) { errors.push(e.message); }
    }

    const ipp = {}, epp = {};
    const mplList = [];

    Object.keys(mauData).map(Number).sort((a,b)=>a-b).forEach((mauIdx) => {
      let direction;
      try { direction = mauDirection(mauIdx); }
      catch (e) { errors.push(e.message); return; }
      const info = mauData[mauIdx];
      // normalize legacy shape
      const traceMap = info.trace || info.segments || {};
      const statMap = info.statistics || {};
      const cats = { trace: {}, statistics: {} };
      const flat = {};
      Object.keys(traceMap).forEach((seg) => {
        const meta = traceMap[seg];
        try {
          const entry = {
            ...meta,
            words_hex: (meta.words || []).map((w) => "0x" + (w >>> 0).toString(16).padStart(8, "0")),
            decoded: decodeSegment(seg, meta.words),
            category: "trace",
          };
          cats.trace[seg] = entry;
          flat[seg] = entry;
        } catch (e) {
          errors.push("mau" + mauIdx + "." + seg + ": " + e.message);
          const entry = { ...meta, error: e.message, category: "trace" };
          cats.trace[seg] = entry;
          flat[seg] = entry;
        }
      });
      Object.keys(statMap).forEach((seg) => {
        const meta = statMap[seg];
        const words = meta.words || [];
        const entry = {
          ...meta,
          words_hex: words.map((w) => "0x" + (w >>> 0).toString(16).padStart(8, "0")),
          decoded: null,
          placeholder: true,
          message: words.length ? "mau 统计格式尚未定义（已保留原始 Domain）" : "mau 统计格式尚未定义",
          category: "statistics",
        };
        cats.statistics[seg] = entry;
        flat["stat:" + seg] = entry;
      });
      const node = { mau: mauIdx, direction, categories: cats, segments: flat };
      (direction === "ipp" ? ipp : epp)["mau" + mauIdx] = node;
    });

    mplRaw.forEach((raw, i) => {
      try {
        mplList.push({
          source: raw.label || ("mpl#" + i),
          decoded: decodeMpl(raw.words),
          word_count: raw.words.length,
        });
      } catch (e) { errors.push("mpl[" + i + "]: " + e.message); }
    });

    const iparserList = iparserRaw.map((raw, i) => {
      try {
        return {
          source: raw.label || ("iparser#" + i),
          decoded: decodeIparser(raw.words),
          word_count: raw.words.length,
        };
      } catch (e) {
        errors.push("iparser[" + i + "]: " + e.message);
        return null;
      }
    }).filter(Boolean);

    return {
      modules: {
        mpl: mplList,
        mau: {
          ipp, epp,
          expected_ipp: IPP.map((i) => "mau" + i),
          expected_epp: EPP.map((i) => "mau" + i),
        },
        iparser: iparserList,
        eparser: { placeholder: true, message: "格式表待定义" },
        pedt: { placeholder: true, message: "格式表待定义" },
      },
      orphans,
      errors,
    };
  }

  /* ---------- UI ---------- */
  const $ = (id) => document.getElementById(id);
  function setStatus(msg, cls) {
    const el = $("parseStatus");
    el.textContent = msg || "";
    el.className = "status" + (cls ? " " + cls : "");
  }

  function setBar(msg) {
    $("statusBar").textContent = msg;
  }

  function collectFields(decoded) {
    if (!decoded) return [];
    if (decoded.fields) return decoded.fields.slice();
    let out = [];
    if (decoded.lama && decoded.lama.fields) {
      out = out.concat(decoded.lama.fields.map((f) => ({ ...f, _group: "lama" })));
    }
    if (decoded.lamb && decoded.lamb.fields) {
      out = out.concat(decoded.lamb.fields.map((f) => ({ ...f, _group: "lamb" })));
    }
    return out;
  }

  function renderFieldTable(fields, title) {
    const hideRsv = $("hideRsv").checked;
    const filter = ($("fieldFilter").value || "").trim().toLowerCase();
    let html = "";
    if (title) html += '<div class="meta">' + escapeHtml(title) + "</div>";
    html += '<table class="fields"><thead><tr>';
    html += "<th>Domain</th><th>Name</th><th>Bits</th><th>W</th><th>Hex</th><th>Dec</th><th>Desc</th>";
    html += "</tr></thead><tbody>";
    fields.forEach((f) => {
      if (hideRsv && f.reserved) return;
      if (filter && String(f.name).toLowerCase().indexOf(filter) < 0) return;
      const cls = f.reserved ? " class=\"rsv\"" : "";
      const dom = f.domain == null ? "—" : "D" + f.domain;
      html += "<tr" + cls + ">";
      html += "<td>" + dom + "</td>";
      html += "<td>" + escapeHtml(f.name) + (f._group ? " <span style=\"color:var(--muted)\">(" + f._group + ")</span>" : "") + "</td>";
      html += "<td>" + escapeHtml(f.bits) + "</td>";
      html += "<td>" + f.width + "</td>";
      html += "<td>" + escapeHtml(f.value_hex) + "</td>";
      html += "<td>" + escapeHtml(String(f.value_dec)) + "</td>";
      html += "<td>" + escapeHtml(f.desc || "") + "</td>";
      html += "</tr>";
    });
    html += "</tbody></table>";
    return html;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[c]);
  }

  function renderPawTable(pawRows) {
    if (!pawRows || !pawRows.length) return "";
    let html = '<div class="paw-hint">Paw：每行 4×u32，左高 bit → 右低 bit</div>';
    html += '<table class="paw-table"><thead><tr><th>Name</th><th>[127:96]</th><th>[95:64]</th><th>[63:32]</th><th>[31:0]</th></tr></thead><tbody>';
    pawRows.forEach((row) => {
      const cells = row.words_hex.slice();
      while (cells.length < 4) cells.push("—");
      html += "<tr><td class=\"paw-name\">" + escapeHtml(row.name) + "</td>";
      cells.slice(0, 4).forEach((c) => { html += "<td>" + escapeHtml(c) + "</td>"; });
      html += "</tr>";
    });
    html += "</tbody></table>";
    return html;
  }

  function renderHalf(half) {
    let html = "";
    if (half.paw_rows && half.paw_rows.length) html += renderPawTable(half.paw_rows);
    html += renderFieldTable(half.fields || [], half.title || "");
    return html;
  }

  function renderDecodedBlock(decoded, extra) {
    if (!decoded) return '<div class="placeholder">无数据</div>';
    if (decoded.error) return '<div class="status err">' + escapeHtml(decoded.error) + "</div>";
    let html = "";
    if (extra) html += extra;
    if (decoded.lama || decoded.lamb) {
      html += '<details class="seg" open><summary>lama</summary><div class="seg-body">';
      html += renderHalf(decoded.lama || {});
      html += "</div></details>";
      html += '<details class="seg" open><summary>lamb</summary><div class="seg-body">';
      html += renderHalf(decoded.lamb || {});
      html += "</div></details>";
      state.lastFields = collectFields(decoded);
    } else {
      if (decoded.paw_rows) html += renderPawTable(decoded.paw_rows);
      html += renderFieldTable(decoded.fields || [], decoded.title || "");
      state.lastFields = decoded.fields || [];
      if (decoded.errors && decoded.errors.length) {
        html += '<div class="status warn">' + escapeHtml(decoded.errors.join("\n")) + "</div>";
      }
    }
    // keygen 附属：按 payloads.mau_mpl_req_data 展示（复用 decodePayload / renderFieldTable）
    if (decoded.mau_mpl_req_data) {
      const p = decoded.mau_mpl_req_data;
      html += '<details class="seg" open><summary>mau_mpl_req_data（payloads）';
      if (p.bitvec_hex) html += " · " + escapeHtml(p.bitvec_hex);
      html += '</summary><div class="seg-body">';
      if (p.note) html += '<div class="meta">' + escapeHtml(p.note) + "</div>";
      html += renderFieldTable(p.fields || [], p.title || "mau_mpl_req_data");
      html += "</div></details>";
      state.lastFields = (state.lastFields || []).concat(p.fields || []);
    }
    return html;
  }

  function renderMauBranch(node, i) {
    const cats = (node && node.categories) || { trace: node && node.segments || {}, statistics: {} };
    const trace = cats.trace || {};
    const stats = cats.statistics || {};
    const has = Object.keys(trace).length + Object.keys(stats).length;
    let html = "<details" + (has ? " open" : "") + "><summary>mau" + i + (has ? "" : " · 空") + "</summary>";
    html += "<details open><summary>trace</summary>";
    TRACE_ORDER.forEach((seg) => {
      if (!trace[seg]) return;
      html += '<button type="button" class="leaf" data-sel="mau:' + i + ":trace:" + seg + '">' + seg + "</button>";
    });
    html += "</details>";
    html += "<details><summary>统计</summary>";
    const statKeys = Object.keys(stats);
    if (!statKeys.length) {
      html += '<div class="meta" style="padding:0.25rem 0.4rem;">（格式待定义）</div>';
    } else {
      statKeys.forEach((seg) => {
        html += '<button type="button" class="leaf" data-sel="mau:' + i + ":stat:" + seg + '">' + seg + "</button>";
      });
    }
    html += "</details></details>";
    return html;
  }

  function renderNav() {
    const root = $("navTree");
    const r = state.result;
    if (!r) { root.innerHTML = ""; return; }
    let html = "";
    const mau = r.modules.mau;
    html += "<details open><summary>mau · ipp</summary>";
    IPP.forEach((i) => { html += renderMauBranch(mau.ipp["mau" + i], i); });
    html += "</details>";
    html += "<details open><summary>mau · epp</summary>";
    EPP.forEach((i) => { html += renderMauBranch(mau.epp["mau" + i], i); });
    html += "</details>";

    html += "<details open><summary>mpl（独立模块）</summary>";
    if (r.modules.mpl && r.modules.mpl.length) {
      r.modules.mpl.forEach((m, idx) => {
        html += '<button type="button" class="leaf" data-sel="mpl:' + idx + '">' +
          escapeHtml(m.source || ("mpl#" + idx)) + "</button>";
      });
    } else {
      html += '<div class="meta" style="padding:0.25rem 0.4rem;">无 mpl 块（用模块=mpl 粘贴，或日志 ---- mpl start ----）</div>';
    }
    html += "</details>";

    html += "<details open><summary>iparser（独立模块）</summary>";
    if (r.modules.iparser && r.modules.iparser.length) {
      r.modules.iparser.forEach((m, idx) => {
        html += '<button type="button" class="leaf" data-sel="iparser:' + idx + '">' +
          escapeHtml(m.source || ("iparser#" + idx)) + "</button>";
      });
    } else {
      html += '<div class="meta" style="padding:0.25rem 0.4rem;">无 iparser 块（用模块=iparser 粘贴，或日志 ---- iparser start ----）</div>';
    }
    html += "</details>";

    if (r.orphans && r.orphans.length) {
      html += "<details open><summary>未归属 / 粘贴结果</summary>";
      r.orphans.forEach((o, idx) => {
        html += '<button type="button" class="leaf" data-sel="orphan:' + idx + '">' +
          escapeHtml(o.name) + " (" + o.word_count + ")</button>";
      });
      html += "</details>";
    }
    root.innerHTML = html;
    root.querySelectorAll("button.leaf").forEach((btn) => {
      btn.addEventListener("click", () => selectNav(btn.getAttribute("data-sel"), btn));
    });
  }

  function selectNav(sel, btn) {
    $("navTree").querySelectorAll("button.leaf").forEach((b) => b.classList.remove("active"));
    if (btn) btn.classList.add("active");
    const parts = sel.split(":");
    const r = state.result;
    const view = $("viewRoot");

    if (parts[0] === "mau") {
      const mau = +parts[1];
      const kind = parts[2]; // trace | stat
      const seg = parts[3];
      state.selection = { type: "mau", mau, kind, seg };
      state.module = "mau";
      syncModuleTab("mau");
      const dir = mauDirection(mau);
      const node = r.modules.mau[dir]["mau" + mau];
      const bucket = kind === "stat" ? "statistics" : "trace";
      const meta = (node.categories && node.categories[bucket] && node.categories[bucket][seg])
        || node.segments[seg];
      let extra = '<div class="meta">mau' + mau + " · " + dir + " · " + bucket + " · " + seg;
      if (meta && meta.word_count != null) extra += " · " + meta.word_count + " Domain";
      extra += "</div>";
      if (!meta) {
        view.innerHTML = '<div class="placeholder">无数据</div>';
      } else if (meta.placeholder) {
        view.innerHTML = extra + '<div class="placeholder">' + escapeHtml(meta.message || "统计格式待定义") + "</div>";
        if (meta.words_hex && meta.words_hex.length) {
          view.innerHTML += '<pre style="font-family:var(--mono);font-size:0.8rem;white-space:pre-wrap;">' +
            escapeHtml(meta.words_hex.join(" ")) + "</pre>";
        }
      } else if (meta.error) {
        view.innerHTML = '<div class="status err">' + escapeHtml(meta.error) + "</div>";
      } else {
        view.innerHTML = renderDecodedBlock(meta.decoded, extra);
      }
      setBar("mau" + mau + " / " + bucket + " / " + seg);
      return;
    }
    if (parts[0] === "mpl") {
      const idx = +parts[1];
      state.selection = { type: "mpl", mplIndex: idx };
      state.module = "mpl";
      syncModuleTab("mpl");
      const m = r.modules.mpl[idx];
      view.innerHTML = renderDecodedBlock(m.decoded,
        '<div class="meta">' + escapeHtml(m.source) +
        (m.decoded.bitvec_hex ? " · " + escapeHtml(m.decoded.bitvec_hex) : "") + "</div>");
      setBar("mpl · " + (m.source || idx));
      return;
    }
    if (parts[0] === "iparser") {
      const idx = +parts[1];
      const m = (r.modules.iparser || [])[idx];
      if (!m) {
        view.innerHTML = '<div class="placeholder">无 iparser 数据</div>';
        setBar("iparser · 无数据");
        return;
      }
      state.selection = { type: "iparser", ipIndex: idx };
      state.module = "iparser";
      syncModuleTab("iparser");
      view.innerHTML = renderDecodedBlock(m.decoded,
        '<div class="meta">' + escapeHtml(m.source) + ' · ' + (m.word_count || 0) + ' words</div>');
      setBar("iparser · " + (m.source || idx));
      return;
    }
    if (parts[0] === "orphan") {
      const idx = +parts[1];
      const o = r.orphans[idx];
      view.innerHTML = o.decoded
        ? renderDecodedBlock(o.decoded, '<div class="meta">orphan · ' + escapeHtml(o.name) + "</div>")
        : '<div class="meta">raw · ' + o.word_count + " words</div><pre style=\"font-family:var(--mono);font-size:0.8rem;white-space:pre-wrap;\">" +
          escapeHtml((o.words_hex || []).join(" ")) + "</pre>";
      setBar("orphan · " + o.name);
    }
  }

  function syncModuleTab(mod) {
    document.querySelectorAll("#moduleTabs button").forEach((b) => {
      b.classList.toggle("active", b.getAttribute("data-mod") === mod);
    });
  }

  function showModule(mod) {
    state.module = mod;
    syncModuleTab(mod);
    const view = $("viewRoot");
    if (mod === "eparser" || mod === "pedt") {
      view.innerHTML = '<div class="placeholder">' + mod + "：格式表待定义（yaml 接入点预留）</div>";
      setBar(mod + " · 占位");
      return;
    }
    if (mod === "iparser") {
      if (!state.result) {
        view.innerHTML = '<div class="placeholder">尚无解析结果</div>';
        return;
      }
      const list = state.result.modules.iparser || [];
      if (!list.length) {
        view.innerHTML = '<div class="placeholder">iparser：未检测到 dump，可粘贴 iparser 文本或 ---- iparser start ---- 日志</div>';
        setBar("iparser · 未检测到数据");
        return;
      }
      const leaf = $("navTree").querySelector('button.leaf[data-sel="iparser:0"]');
      selectNav("iparser:0", leaf);
      return;
    }
    if (!state.result) {
      view.innerHTML = '<div class="placeholder">尚无解析结果</div>';
      return;
    }
    if (mod === "mpl") {
      const list = state.result.modules.mpl;
      if (!list.length) {
        view.innerHTML = '<div class="placeholder">无 mpl 数据（mpl 为独立模块，请粘贴 mpl dump 或日志中的 mpl 块）</div>';
        return;
      }
      const leaf = $("navTree").querySelector('button.leaf[data-sel="mpl:0"]');
      selectNav("mpl:0", leaf);
      return;
    }
    // mau: 选第一个有数据的
    const mau = state.result.modules.mau;
    let found = null;
    IPP.concat(EPP).some((i) => {
      const dir = i <= 8 ? "ipp" : "epp";
      const node = mau[dir]["mau" + i];
      if (!node) return false;
      const trace = (node.categories && node.categories.trace) || node.segments || {};
      const segs = Object.keys(trace);
      if (!segs.length) return false;
      const seg = TRACE_ORDER.find((s) => trace[s]) || segs[0];
      found = { i, seg };
      return true;
    });
    if (found) {
      const leaf = $("navTree").querySelector(
        'button.leaf[data-sel="mau:' + found.i + ":trace:" + found.seg + '"]'
      );
      selectNav("mau:" + found.i + ":trace:" + found.seg, leaf);
    } else if (state.result.orphans && state.result.orphans.length) {
      const leaf = $("navTree").querySelector('button.leaf[data-sel="orphan:0"]');
      selectNav("orphan:0", leaf);
    } else {
      view.innerHTML = '<div class="placeholder">日志中未识别到 mau 子段；解析后请在左侧选择 mau 实例</div>';
    }
  }

  function emptyMauMaps() {
    return { ipp: {}, epp: {}, expected_ipp: IPP.map((i)=>"mau"+i), expected_epp: EPP.map((i)=>"mau"+i) };
  }

  function doParse() {
    const text = $("pasteArea").value;
    const mod = $("pasteModule").value;
    setStatus("");
    try {
      let result;
      if (mod === "auto") {
        result = parseLog(text);
      } else if (mod === "mpl") {
        const words = parseU32Tokens(text);
        const decoded = decodeMpl(words);
        result = {
          modules: {
            mpl: [{ source: "paste", decoded, word_count: words.length }],
            mau: emptyMauMaps(),
            iparser: [],
            eparser: { placeholder: true, message: "格式表待定义" },
            pedt: { placeholder: true, message: "格式表待定义" },
          },
          orphans: [],
          errors: [],
        };
      } else if (mod === "iparser") {
        const words = parseU32Tokens(text);
        const decoded = decodeIparser(words);
        result = {
          modules: {
            mpl: [],
            mau: emptyMauMaps(),
            iparser: [{ source: "paste", decoded, word_count: words.length }],
            eparser: { placeholder: true, message: "格式表待定义" },
            pedt: { placeholder: true, message: "格式表待定义" },
          },
          orphans: [],
          errors: [],
        };
      } else {
        // mau 粘贴：不在解析时选实例，放入「未归属」；解析后在导航中查看
        const words = parseU32Tokens(text);
        const seg = $("pasteSegment").value;
        const decoded = decodeSegment(seg, words);
        result = {
          modules: {
            mpl: [],
            mau: emptyMauMaps(),
            iparser: [],
            eparser: { placeholder: true, message: "格式表待定义" },
            pedt: { placeholder: true, message: "格式表待定义" },
          },
          orphans: [{
            name: seg,
            word_count: words.length,
            words_hex: words.map((w) => "0x" + (w >>> 0).toString(16).padStart(8, "0")),
            category: "trace",
            decoded,
          }],
          errors: [],
        };
      }
      state.result = result;
      renderNav();
      const errs = result.errors || [];
      if (errs.length) setStatus(errs.join("\n"), "warn");
      else setStatus("解析完成 — 请在左侧选择模块 / 子段", "");
      showModule(state.module === "eparser" || state.module === "pedt" ? state.module : state.module);
      setBar("解析完成 · mau ipp=" + Object.keys(result.modules.mau.ipp).length +
        " epp=" + Object.keys(result.modules.mau.epp).length +
        " mpl=" + result.modules.mpl.length +
        " iparser=" + ((result.modules.iparser || []).length) +
        " orphan=" + (result.orphans || []).length);
    } catch (e) {
      setStatus(String(e.message || e), "err");
      setBar("解析失败");
    }
  }

  function exportCsv() {
    const fields = state.lastFields || [];
    if (!fields.length) { setStatus("当前无可导出字段", "warn"); return; }
    const hideRsv = $("hideRsv").checked;
    const filter = ($("fieldFilter").value || "").trim().toLowerCase();
    const lines = ["domain,name,bits,width,hex,dec,desc"];
    fields.forEach((f) => {
      if (hideRsv && f.reserved) return;
      if (filter && String(f.name).toLowerCase().indexOf(filter) < 0) return;
      const row = [
        f.domain == null ? "" : f.domain,
        f.name,
        f.bits,
        f.width,
        f.value_hex,
        f.value_dec,
        '"' + String(f.desc || "").replace(/"/g, '""') + '"',
      ];
      lines.push(row.join(","));
    });
    const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "trace_fields.csv";
    a.click();
    URL.revokeObjectURL(a.href);
  }

  $("btnParse").addEventListener("click", doParse);
  $("btnClear").addEventListener("click", () => {
    $("pasteArea").value = "";
    $("fileInput").value = "";
    state.result = null;
    state.lastFields = [];
    $("navTree").innerHTML = "";
    $("viewRoot").innerHTML = '<div class="placeholder">粘贴 hex 或选择日志文件后点击「解析」</div>';
    setStatus("");
    setBar("已清空");
  });
  $("btnExport").addEventListener("click", exportCsv);
  $("fieldFilter").addEventListener("input", () => {
    if (state.selection) {
      const sel = state.selection;
      let key;
      if (sel.type === "mau") key = "mau:" + sel.mau + ":" + (sel.kind || "trace") + ":" + sel.seg;
      else if (sel.type === "mpl") key = "mpl:" + sel.mplIndex;
      if (key) {
        const leaf = $("navTree").querySelector('button.leaf[data-sel="' + key + '"]');
        selectNav(key, leaf);
      }
    }
  });
  $("hideRsv").addEventListener("change", () => $("fieldFilter").dispatchEvent(new Event("input")));

  $("fileInput").addEventListener("change", (ev) => {
    const f = ev.target.files && ev.target.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = () => {
      $("pasteArea").value = String(reader.result || "");
      $("pasteModule").value = "auto";
      setStatus("已载入 " + f.name + "，点击解析", "");
    };
    reader.onerror = () => setStatus("读文件失败", "err");
    reader.readAsText(f);
  });

  document.querySelectorAll("#moduleTabs button").forEach((b) => {
    b.addEventListener("click", () => showModule(b.getAttribute("data-mod")));
  });

  // 预嵌入结果
  if (window.TRACE_RESULT) {
    state.result = window.TRACE_RESULT;
    renderNav();
    showModule("mau");
    setBar("已加载预解析结果");
  }
})();
  