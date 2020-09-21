#include "DepletedComposition.h"

#include <iostream>
#include <cstdlib>

#include "TMath.h"

ClassImp(DepletedComposition);

using namespace std;

DepletedComposition::DepletedComposition()
{
  name = "";
  volume = 0.;
  local_burnup = 0.;
  power = 0.;
  fast_flux = 0.;
  therm_flux = 0.;
}

void DepletedComposition::clear()
{
  name = "";
  volume = 0.;
  local_burnup = 0.;
  power = 0.;
  fast_flux = 0.;
  therm_flux = 0.;
  mass.clear();
  concentration.clear();
  activity.clear();
  reactionrates.clear();
}

void DepletedComposition::DumpGlobals() const
{

  cout << endl;
  cout << "** Dumping DepletionComposition : " << name << endl;
  cout << "volume = " << volume << endl;
  cout << "local_burnup = " << local_burnup << endl;
  cout << "power = " << power << endl;
  cout << "fast_flux = " << fast_flux << endl;
  cout << "therm_flux = " << therm_flux << endl;
  cout << endl;

}

void DepletedComposition::DumpMass() const
{

  cout << endl;
  map<TString,double>::const_iterator it;
  for (it=mass.begin();it!=mass.end();it++)
    cout << it->first << "  " << it->second << endl;
  cout << endl;

}

void DepletedComposition::DumpIsotopes() const
{
  cout << endl;
  map<TString,double>::const_iterator it;
    for (it=mass.begin();it!=mass.end();it++) {
      cout << it->first << ", ";
  }
  cout << endl << endl;
}

void DepletedComposition::DumpReactionNames() const
{
  cout << endl;
  map<TString,double>::const_iterator it;
    for (it=reactionrates.begin();it!=reactionrates.end();it++) {
      cout << it->first << ", ";
  }
  cout << endl << endl;
}

DepletedComposition DepletedComposition::operator +(const DepletedComposition & a)
{

  if (GetCompoName()!=a.GetCompoName()) {
    cout << "Impossible to sum compositions which composition names are different" << endl;
    exit(1);
  }

  DepletedComposition res;
  res.SetName(GetCompoName());
  res.SetVolume(GetVolume()+a.GetVolume());
  res.SetLocalBurnup(GetLocalBurnup()+a.GetLocalBurnup());
  res.SetPower(GetPower()+a.GetPower());
  res.SetFastFlux(GetFastFlux()+a.GetFastFlux());
  res.SetThermFlux(GetThermFlux()+a.GetThermFlux());
  map<TString,double>::iterator it;
  for (it=mass.begin();it!=mass.end();it++) {
    res.SetMass(it->first,GetMass(it->first)+a.GetMass(it->first));
    res.SetConcentration(it->first,GetConcentration(it->first)+a.GetConcentration(it->first));
    res.SetActivity(it->first,GetActivity(it->first)+a.GetActivity(it->first));
  }
  for (it=reactionrates.begin();it!=reactionrates.end();it++) {
    // cout << "reaction rates:" << it->first << endl;
    res.SetReactionRate(it->first,GetReactionRate(it->first)+a.GetReactionRate(it->first));
    res.SetThermalReactionRate(it->first,GetThermalReactionRate(it->first)+a.GetThermalReactionRate(it->first));
    res.SetFastReactionRate(it->first,GetFastReactionRate(it->first)+a.GetFastReactionRate(it->first));
    // res.SetIsotopeReactionName()
  }
  set<TString>::iterator jt, kt;
  for (jt=isotope_names.begin(); jt!=isotope_names.end(); jt++) {
    res.SetIsotopeName(*jt);
    for (kt=iso_reac_names[*jt].begin(); kt!=iso_reac_names[*jt].end(); kt++) {
      res.SetIsotopeReactionName(*jt, *kt);
    }
  }
  set<TString> aisonames = a.GetIsotopesNames();
  for (jt=aisonames.begin(); jt!=aisonames.end(); jt++) {
    res.SetIsotopeName(*jt);
    set<TString> airnames = a.GetReactionNames(*jt);
    for (kt=airnames.begin(); kt!=airnames.end(); kt++) {
      res.SetIsotopeReactionName(*jt, *kt);
    }
  }

  return res;

}

DepletedComposition DepletedComposition::operator -(const DepletedComposition & a)
{

  if (GetCompoName()!=a.GetCompoName()) {
    cout << "Impossible to substract compositions which composition names are different" << endl;
    exit(1);
  }

  DepletedComposition res;
  res.SetName(GetCompoName());
  res.SetVolume(GetVolume()-a.GetVolume());
  res.SetLocalBurnup(GetLocalBurnup()-a.GetLocalBurnup());
  res.SetPower(GetPower()-a.GetPower());
  res.SetFastFlux(GetFastFlux()-a.GetFastFlux());
  res.SetThermFlux(GetThermFlux()-a.GetThermFlux());
  map<TString,double>::iterator it;
  for (it=mass.begin();it!=mass.end();it++) {
    res.SetMass(it->first,GetMass(it->first)-a.GetMass(it->first));
    res.SetConcentration(it->first,GetConcentration(it->first)-a.GetConcentration(it->first));
    res.SetActivity(it->first,GetActivity(it->first)-a.GetActivity(it->first));
  }
  for (it=reactionrates.begin();it!=reactionrates.end();it++) {
    res.SetReactionRate(it->first,GetReactionRate(it->first)-a.GetReactionRate(it->first));
    res.SetThermalReactionRate(it->first,GetThermalReactionRate(it->first)-a.GetThermalReactionRate(it->first));
    res.SetFastReactionRate(it->first,GetFastReactionRate(it->first)-a.GetFastReactionRate(it->first));
  }
  set<TString>::iterator jt, kt;
  for (jt=isotope_names.begin(); jt!=isotope_names.end(); jt++) {
    res.SetIsotopeName(*jt);
    for (kt=iso_reac_names[*jt].begin(); kt!=iso_reac_names[*jt].end(); kt++) {
      res.SetIsotopeReactionName(*jt, *kt);
    }
  }
  set<TString> aisonames = a.GetIsotopesNames();
  for (jt=aisonames.begin(); jt!=aisonames.end(); jt++) {
    res.SetIsotopeName(*jt);
    set<TString> airnames = a.GetReactionNames(*jt);
    for (kt=airnames.begin(); kt!=airnames.end(); kt++) {
      res.SetIsotopeReactionName(*jt, *kt);
    }
  }

  return res;
}

DepletedComposition DepletedComposition::operator *(const DepletedComposition & a)
{

  if (GetCompoName()!=a.GetCompoName()) {
    cout << "Impossible to sum compositions which composition names are different" << endl;
    exit(1);
  }

  DepletedComposition res;
  res.SetName(GetCompoName());
  res.SetVolume(GetVolume()*a.GetVolume());
  res.SetLocalBurnup(GetLocalBurnup()*a.GetLocalBurnup());
  res.SetPower(GetPower()*a.GetPower());
  res.SetFastFlux(GetFastFlux()*a.GetFastFlux());
  res.SetThermFlux(GetThermFlux()*a.GetThermFlux());
  map<TString,double>::iterator it;
  for (it=mass.begin();it!=mass.end();it++) {
    res.SetMass(it->first,GetMass(it->first)*a.GetMass(it->first));
    res.SetConcentration(it->first,GetConcentration(it->first)*a.GetConcentration(it->first));
    res.SetActivity(it->first,GetActivity(it->first)*a.GetActivity(it->first));
  }
  for (it=reactionrates.begin();it!=reactionrates.end();it++) {
    res.SetReactionRate(it->first,GetReactionRate(it->first)*a.GetReactionRate(it->first));
    res.SetThermalReactionRate(it->first,GetThermalReactionRate(it->first)*a.GetThermalReactionRate(it->first));
    res.SetFastReactionRate(it->first,GetFastReactionRate(it->first)*a.GetFastReactionRate(it->first));
  }
  set<TString>::iterator jt, kt;
  for (jt=isotope_names.begin(); jt!=isotope_names.end(); jt++) {
    res.SetIsotopeName(*jt);
    for (kt=iso_reac_names[*jt].begin(); kt!=iso_reac_names[*jt].end(); kt++) {
      res.SetIsotopeReactionName(*jt, *kt);
    }
  }
  set<TString> aisonames = a.GetIsotopesNames();
  for (jt=aisonames.begin(); jt!=aisonames.end(); jt++) {
    res.SetIsotopeName(*jt);
    set<TString> airnames = a.GetReactionNames(*jt);
    for (kt=airnames.begin(); kt!=airnames.end(); kt++) {
      res.SetIsotopeReactionName(*jt, *kt);
    }
  }
  return res;
}

DepletedComposition DepletedComposition::operator /(double div)
{

  if (div==0.) {
    cout << "Division by 0 ..." << endl;
    exit(1);
  }

  DepletedComposition res;
  res.SetName(GetCompoName());
  res.SetVolume(GetVolume()/div);
  res.SetLocalBurnup(GetLocalBurnup()/div);
  res.SetPower(GetPower()/div);
  res.SetFastFlux(GetFastFlux()/div);
  res.SetThermFlux(GetThermFlux()/div);
  map<TString,double>::iterator it;
  for (it=mass.begin();it!=mass.end();it++) {
    res.SetMass(it->first,GetMass(it->first)/div);
    res.SetConcentration(it->first,GetConcentration(it->first)/div);
    res.SetActivity(it->first,GetActivity(it->first)/div);
  }
  for (it=reactionrates.begin();it!=reactionrates.end();it++) {
    res.SetReactionRate(it->first,GetReactionRate(it->first)/div);
    res.SetThermalReactionRate(it->first,GetThermalReactionRate(it->first)/div);
    res.SetFastReactionRate(it->first,GetFastReactionRate(it->first)/div);
  }
  set<TString>::iterator jt, kt;
  for (jt=isotope_names.begin(); jt!=isotope_names.end(); jt++) {
    res.SetIsotopeName(*jt);
    for (kt=iso_reac_names[*jt].begin(); kt!=iso_reac_names[*jt].end(); kt++) {
      res.SetIsotopeReactionName(*jt, *kt);
    }
  }

  return res;
}

DepletedComposition DepletedComposition::Sqrt()
{

  DepletedComposition res;
  res.SetName(GetCompoName());
  res.SetVolume(TMath::Sqrt(GetVolume()));
  res.SetLocalBurnup(TMath::Sqrt(GetLocalBurnup()));
  res.SetPower(TMath::Sqrt(GetPower()));
  res.SetFastFlux(TMath::Sqrt(GetFastFlux()));
  res.SetThermFlux(TMath::Sqrt(GetThermFlux()));
  map<TString,double>::iterator it;
  for (it=mass.begin();it!=mass.end();it++) {
    cout << "isotope:" << it->first << endl;
    res.SetIsotopeName(it->first);
    res.SetMass(it->first,TMath::Sqrt(GetMass(it->first)));
    res.SetConcentration(it->first,TMath::Sqrt(GetConcentration(it->first)));
    res.SetActivity(it->first,TMath::Sqrt(GetActivity(it->first)));
  }
  for (it=reactionrates.begin();it!=reactionrates.end();it++) {
    res.SetReactionRate(it->first,TMath::Sqrt(GetReactionRate(it->first)));
    res.SetThermalReactionRate(it->first,TMath::Sqrt(GetThermalReactionRate(it->first)));
    res.SetFastReactionRate(it->first,TMath::Sqrt(GetFastReactionRate(it->first)));
  }
  set<TString>::iterator jt, kt;
  for (jt=isotope_names.begin(); jt!=isotope_names.end(); jt++) {
    res.SetIsotopeName(*jt);
    for (kt=iso_reac_names[*jt].begin(); kt!=iso_reac_names[*jt].end(); kt++) {
      res.SetIsotopeReactionName(*jt, *kt);
    }
  }

  return res;
}

double DepletedComposition::GetMass(TString isoname) const
{
  map<TString, double>::const_iterator it = mass.find(isoname);
  if (it==mass.end()) {
    cout << "DepletedComposition::GetMass WARNING Isotope " << isoname;
    cout << " is not present in composition " << name << endl;
  }
  return it==mass.end() ? 0. : it->second ;
}

double DepletedComposition::GetConcentration(TString isoname) const
{
  map<TString, double>::const_iterator it = concentration.find(isoname);
  if (it==concentration.end()) {
    cout << "DepletedComposition::GetConcentration WARNING Isotope " << isoname;
    cout << " is not present in composition " << name << endl;
  }
  return it==concentration.end() ? 0. : it->second ;
}

double DepletedComposition::GetActivity(TString isoname) const
{
  map<TString, double>::const_iterator it = activity.find(isoname);
  if (it==activity.end()) {
    cout << "DepletedComposition::GetActivity WARNING Isotope " << isoname;
    cout << " is not present in composition " << name << endl;
  }
  return it==activity.end() ? 0. : it->second ;
}

double DepletedComposition::GetReactionRate(TString reactionname) const
{
  map<TString, double>::const_iterator it = reactionrates.find(reactionname);
  if (it==reactionrates.end()) {
    cout << "DepletedComposition::GetReactionRate WARNING IsoReaction " << reactionname;
    cout << " is not present in composition " << name << endl;
  }
  return it==reactionrates.end() ? 0. : it->second ;
}

double DepletedComposition::GetThermalReactionRate(TString reactionname) const
{
  map<TString, double>::const_iterator it = thermal_reactionrates.find(reactionname);
  if (it==thermal_reactionrates.end()) {
    cout << "DepletedComposition::GetThermalReactionRate WARNING IsoReaction " << reactionname;
    cout << " is not present in composition " << name << endl;
  }
  return it==thermal_reactionrates.end() ? 0. : it->second ;
}

double DepletedComposition::GetFastReactionRate(TString reactionname) const
{
  map<TString, double>::const_iterator it = fast_reactionrates.find(reactionname);
  if (it==fast_reactionrates.end()) {
    cout << "DepletedComposition::GetFastReactionRate WARNING IsoReaction " << reactionname;
    cout << " is not present in composition " << name << endl;
  }
  return it==fast_reactionrates.end() ? 0. : it->second ;
}
