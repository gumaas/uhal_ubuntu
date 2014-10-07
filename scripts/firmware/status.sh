#!/bin/bash    

pushd ..

svn status --show-updates mp7_690es/*
svn status --show-updates ipbus/*
svn status --show-updates mp7_ctrl/*
svn status --show-updates mp7_counters/*
svn status --show-updates mp7_xpoint/*
svn status --show-updates opencores_i2c/*
svn status --show-updates mp7_ttc/*
svn status --show-updates mp7_mgt/*
svn status --show-updates mp7_counters/*
svn status --show-updates mp7_buffers/*
svn status --show-updates mp7_algo/*
svn status --show-updates mp7_preproc/*
# svn status --show-updates calol2/*

popd