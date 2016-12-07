select City.Name, City.Population, Country.Population
    from Country
    inner join City on Country.Code = City.CountryCode
    order by (1.0 * City.Population / 1.0 * Country.Population) desc, City.Name desc
    limit 20;
