// command line
//BoostedTau_limit_single_plus_CR_newUL --year=2018 --bin=bin0 --WP=T --DIR=tgp_v1

#include <string>
#include <map>
#include <set>
#include <iostream>
#include <vector>
#include <utility>
#include <cstdlib>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "boost/lexical_cast.hpp"
#include "boost/regex.hpp"
#include "boost/filesystem.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
#include "CombineHarvester/CombineTools/interface/CardWriter.h"
#include "CombineHarvester/CombineTools/interface/CopyTools.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"

namespace po = boost::program_options;
using boost::starts_with;
using namespace std;

int main(int argc, char** argv) {


    string postfix="";

    string year = "2016";
    string inputFile="";
    string WP="WP";
    string bin="bin";
    string DIR="DIR";

    po::variables_map vm;
    po::options_description config("configuration");
    config.add_options()
      ("year", po::value<string>(&year)->default_value("2016"))
      ("WP", po::value<string>(&WP)->default_value(""))
      ("bin", po::value<string>(&bin)->default_value(""))
      ("inputFile", po::value<string>(&inputFile)->default_value(""))
      ("DIR", po::value<string>(&DIR)->default_value(""));
    po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
    po::notify(vm);








    //! [part1]
    // First define the location of the "auxiliaries" directory where we can
    // source the input files containing the datacard shapes
//    string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";
    string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/bin/aux/";
    
    // Create an empty CombineHarvester instance that will hold all of the
    // datacard configuration and histograms etc.
    ch::CombineHarvester cb;
    
    typedef vector<pair<int, string>> Categories;
    typedef vector<string> VString;
    // Uncomment this next line to see a *lot* of debug information
    // cb.SetVerbosity(3);
    
    // Here we will just define two categories for an 8TeV analysis. Each entry in
    // the vector below specifies a bin name and corresponding bin_id.
    
    VString chns = { "sig_high","sig_low","cr_tt","cr_fake", "cr_z"};
    
    map<string, string> input_folders = {
        {"sig_high", "."},
        {"sig_low", "."},
        {"cr_tt", "."},
        {"cr_fake", "."},
	{"cr_z", "."}
    };
    
    map<string, VString> bkg_procs;
    bkg_procs["sig_high"] = {"DY", "TTT","VV","ZZ","WJets"};
    bkg_procs["sig_low"] = {"DY", "TTT","VV","ZZ","WJets"};
    bkg_procs["cr_tt"] = {"DY", "TTT","VV","ZZ","WJets"};
    bkg_procs["cr_fake"] = {"DY", "TTT","VV","ZZ","WJets"};
    bkg_procs["cr_z"] = {"DY", "TTT","VV","ZZ","WJets"};


    VString sig_procs = {"Radion_4Tau_"};
    
    map<string, Categories> cats;
    //cats["et_13TeV"] = {
    //      {1, "EleTau_DiJet"}};
    
    
    cats["sig_high"] = {
        {1, "highPurity_0jet"},
//        {2, "fail"}
    };
    cats["sig_low"] = {
        {1, "lowPurity_0jet"},
//        {2, "fail"}
    };
    cats["cr_tt"] = {
        {1, "TTCR_0jet"},
//        {2, "fail"}
    };
    cats["cr_z"] = {
        {1, "ZCR_0jet"},
    };
    cats["cr_fake"] = {
        {1, "fakeCR_0jet"},
//        {2, "fail"}
    };
    
    
    
    // ch::Categories is just a typedef of vector<pair<int, string>>
    //! [part1]
    
    
    //! [part2]
        //vector<string> masses = ch::MassesFromRange("1000-3000:1000");
        //vector<string> masses = ch::MassesFromRange("1-3:1");
		vector<string> masses = {"1","1.5","2","2.5","3"};
    //    vector<string> masses = ch::MassesFromRange("14-15:1");
    //vector<string> masses = ch::MassesFromRange("14-15:1");
//    vector<string> masses = {"125"};
    // Or equivalently, specify the mass points explicitly:
    //! [part2]
    
    
    //! [part4]
    
    for (auto chn : chns) {
        cb.AddObservations(
                           {"*"}, {"Radion_4Tau_"}, {"13TeV"}, {chn}, cats[chn]);
        cb.AddProcesses(
                        {"*"}, {"Radion_4Tau_"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn], false);
        cb.AddProcesses(
                        masses, sig_procs, {"13TeV"}, {chn}, sig_procs, cats[chn], true);
    }
    
    
    
    
    cout << ">> Extracting histograms from input root files...\n";
    for (string era : {"13TeV"}) {
        for (string chn : chns) {
//            /mt2017_vis_masslep2IsoPassV_bin2.root
            string file = aux_shapes + "HH4t_Withp5Masses.root";

//            string file = aux_shapes + input_folders[chn] + "/newtemplate_boostedH_"+chn+"_"+year+"_"+WP+".root";
//            if (chn.find("mm") != string::npos ) file = aux_shapes + "boostedHTT_"+chn+"_"+year+".input.root";
            cb.cp().channel({chn}).era({era}).backgrounds().ExtractShapes(
                                                                          file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
            cb.cp().channel({chn}).era({era}).signals().ExtractShapes(
                                                                      file, "$BIN/$PROCESS$MASS", "$BIN/$PROCESS$MASS_$SYSTEMATIC");
        }
    }
    
    
    //Some of the code for this is in a nested namespace, so
    // we'll make some using declarations first to simplify things a bit.
    using ch::syst::SystMap;
    using ch::syst::era;
    using ch::syst::bin_id;
    using ch::syst::process;
    using ch::JoinStr;
    
    
    // Norm systematics
    
    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"WJets", "TT","VV"}}))
    .AddSyst(cb, "CMS_lumi_$ERA", "lnN", SystMap<era>::init({"13TeV"}, 1.024));
    
    
    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"WJets", "TT","VV"}}))
    .AddSyst(cb, "CMS_eff_m$ERA", "lnN", SystMap<era>::init({"13TeV"}, 1.02));
    
    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"WJets", "TT","VV"}}))
    .AddSyst(cb, "CMS_trg_m$ERA", "lnN", SystMap<era>::init({"13TeV"}, 1.02));


    // cb.cp().channel({"mm"}).process(ch::JoinStr({sig_procs, {"W", "TT","VV"}}))
    // .AddSyst(cb, "CMS_lumi_$ERA", "lnN", SystMap<era>::init({"13TeV"}, 1.024));
        
    
    // cb.cp().channel({"mm"}).process(ch::JoinStr({sig_procs, {"W", "TT","VV"}}))
    // .AddSyst(cb, "CMS_eff_m$ERA", "lnN", SystMap<era>::init({"13TeV"}, 1.02));
    
    // cb.cp().channel({"mm"}).process(ch::JoinStr({sig_procs, {"W", "TT","VV"}}))
    // .AddSyst(cb, "CMS_trg_m$ERA", "lnN", SystMap<era>::init({"13TeV"}, 1.02));



//    cb.cp().process({"DYJets"})
//    .AddSyst(cb, "CMS_htt_ZTTNorm", "lnN", SystMap<>::init(1.10));
    
    cb.cp().process({"TT"})
    .AddSyst(cb, "CMS_htt_TTNorm", "lnN", SystMap<>::init(1.10));
    
    cb.cp().process({"VV"})
    .AddSyst(cb, "CMS_htt_VVNorm", "lnN", SystMap<>::init(1.10));
    
//    cb.cp().process({"ZLL"})
//    .AddSyst(cb, "CMS_htt_ZLLNorm", "lnN", SystMap<>::init(1.10));
//
//    cb.cp().process({"ZJ"})
//    .AddSyst(cb, "CMS_htt_ZJNorm", "lnN", SystMap<>::init(1.10));
    
    cb.cp().process({"WJets"})
    .AddSyst(cb, "CMS_htt_WNorm", "lnN", SystMap<>::init(1.10));
    
    cb.cp().process({"QCD"})
    .AddSyst(cb, "CMS_htt_QCDNorm", "lnN", SystMap<>::init(1.20));
    
    
    // Shape systematics
    
//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"W", "TT","VV"}}))
//    .AddSyst(cb, "met_JES", "shape", SystMap<>::init(1.00));
//
//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"W", "TT","VV"}}))
//    .AddSyst(cb, "met_UES", "shape", SystMap<>::init(1.00));

//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"ZLL","ZJ"}}))
//    .AddSyst(cb, "dyShape_", "shape", SystMap<>::init(1.00));
//
//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"ZLL","ZJ"}}))
//    .AddSyst(cb, "zmumuShape_", "shape", SystMap<>::init(1.00));
//
//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"TT","VV","WJets"}}))
//    .AddSyst(cb, "JES", "shape", SystMap<>::init(1.00));
//
//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"TT","VV","WJets"}}))
//    .AddSyst(cb, "MissingEn_UES", "shape", SystMap<>::init(1.00));
//
//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"TT","VV","WJets"}}))
//    .AddSyst(cb, "MissingEn_JES", "shape", SystMap<>::init(1.00));


//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"TT","VV"}}))
//    .AddSyst(cb, "en_scale_", "shape", SystMap<>::init(1.00));

//    cb.cp().channel({"mt"}).process(ch::JoinStr({sig_procs, {"TT","VV"}}))
//    .AddSyst(cb, "prefire", "shape", SystMap<>::init(1.00));

 //   cb.cp().channel({"mt"}).process({sig_procs})
 //   .AddSyst(cb, "Z_masspt_", "shape", SystMap<>::init(1.00));


//    cb.cp().channel({"mt"}).process({"QCD"})
//    .AddSyst(cb, "shape_", "shape", SystMap<>::init(1.00));

//    cb.cp().channel({"mt"}).process({"TT"})
//    .AddSyst(cb, "ttbarShape_", "shape", SystMap<>::init(1.00));

    
    cout << ">> Adding systematic uncertainties...\n";
    //cout << "...Or Not" << endl;
    cb.cp().backgrounds().ExtractShapes(
                                        //aux_shapes + "/HH4t_new.root",
                                        aux_shapes + "/HH4t_new_UL.root",
                                        "$BIN/$PROCESS",
                                        "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().signals().ExtractShapes(
                                        //aux_shapes + "/HH4t_new.root",
                                        aux_shapes + "/HH4t_new_UL.root",
                                    "$BIN/$PROCESS$MASS",
                                    "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    
    //! [part7]
    
    
    
    
    
    //! [part7]
    
    //! [part8]
    //    auto bbb = ch::BinByBinFactory()
    //    .SetAddThreshold(0.1)
    //    .SetFixNorm(true);
    
    //    bbb.AddBinByBin(cb.cp().backgrounds(), cb);
    
    // This function modifies every entry to have a standardised bin name of
    // the form: {analysis}_{channel}_{bin_id}_{era}
    // which is commonly used in the htt analyses
    ch::SetStandardBinNames(cb);
    
    
    
    //! [part8]
    
    //! [part9]
    // First we generate a set of bin names:
    set<string> bins = cb.bin_set();
    // This method will produce a set of unique bin names by considering all
    // Observation, Process and Systematic entries in the CombineHarvester
    // instance.
    
    // We create the output root file that will contain all the shapes.
    //TFile output("RHW_mt.inputs.root", "RECREATE");
    
    // Finally we iterate through each bin,mass combination and write a
    
    
    auto pre_drop = cb.syst_name_set();
    //cb.syst_name(droplist, false);
    auto post_drop = cb.syst_name_set();
    cout << ">> Systematics dropped: " << pre_drop.size() - post_drop.size()
    << "\n";
    
    
    string folder = DIR+"/"+year+"_"+WP+"_"+bin;
    boost::filesystem::create_directories(folder);
    boost::filesystem::create_directories(folder + "/common");
    for (auto m : masses) {
        boost::filesystem::create_directories(folder + "/" + m);
    }
    
    for (string chn : chns) {
        TFile output((folder + "/common/"+chn+".root").c_str(),
                     "RECREATE");
        auto bins = cb.cp().channel({chn}).bin_set();
        for (auto b : bins) {
            for (auto m : masses) {
                cout << ">> Writing datacard for bin: " << b << " and mass: " << m
                << "\r" << flush;
                cb.cp().channel({chn}).bin({b}).mass({m, "*"}).WriteDatacard(
                                                                             folder + "/" + m + "/" + b + ".txt", output);
            }
        }
        output.Close();
    }
    
    
    //! [part9]
    
}
