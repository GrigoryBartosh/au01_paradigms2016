select First.Year, Second.Year, Country.Name, (1.0 * (Second.Rate - First.Rate) / 1.0 * (Second.Year - First.Year)) as Mul
    from Country
    inner join LiteracyRate First on Country.Code = First.CountryCode
    inner join LiteracyRate Second on Country.Code = Second.CountryCode
    inner join LiteracyRate Thirt on Country.Code = Thirt.CountryCode
    where First.Year <= Thirt.Year and Thirt.Year < Second.Year
    group by Country.Name, First.Year, Second.Year
    having max(Thirt.Year) = First.Year
    order by Mul desc;
